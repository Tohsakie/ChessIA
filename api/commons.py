

import torch
import torch.nn as nn
import numpy as np
import pandas as pd

import chess
import chess.svg
from IPython.display import display


PIECE_TO_INT_2 = {key: i for i, key in enumerate(["r", "n", "b", "q", "k", "p", "R", "N", "B", "Q", "K", "P"])}
def transform_fen(inp_fen:str) -> torch.Tensor:
    board_tensor = []
    for i, piece in enumerate(PIECE_TO_INT_2.keys()):
        piece_matrix = []
        for row in inp_fen.split("/"):
            row_vec = []
            assert isinstance(row, str)
            for element in row:
                if element.isalpha():
                    if element == piece:
                        row_vec += [1]
                    else:
                        row_vec += [0]
                else:
                    if element.isdigit():
                        row_vec += int(element) * [0]  
                    else:
                        raise ValueError 
            assert len(row_vec) == 8
            piece_matrix.append(row_vec)
        assert len(piece_matrix) == 8
        board_tensor.append(piece_matrix)
    assert len(board_tensor) == 12
    return torch.ByteTensor(board_tensor)

CASTLE_TO_INT = {key: i for i, key in enumerate(["K", "Q", "k", "q"])}
def castle_to_vec(inp_castle_str):
    out_vec = 4 * [0]
    if inp_castle_str != "-":
        for side in inp_castle_str:
            out_vec[CASTLE_TO_INT[side]] = 1
    return torch.ByteTensor(out_vec)

TURN_TO_INT = {"w": 0, "b": 1}
ENPASSANT_TO_INT = {key: str(i + 1) for i, key in enumerate(["a", "b", "c", "d", "e", "f", "g", "h"])}
def en_passant_to_vec(inp_en_passant):
    output_tensor = torch.zeros([8, 8], dtype=torch.uint8)
    if inp_en_passant != "-":
        assert len(inp_en_passant) == 2
        assert inp_en_passant[0].isalpha()
        assert inp_en_passant[1].isdigit()
        square = (int(ENPASSANT_TO_INT[inp_en_passant[0]])-1, int(inp_en_passant[1])-1)
        assert isinstance(square, tuple)
        output_tensor[7-square[1],square[0]] = 1
    return output_tensor

TURN_TO_INT = {"w": 0, "b": 1}
def encode_fen_flat(inp_fen_string):
    board_str, turn_str, castling_str, enpassant_str, _, _ = inp_fen_string.split(" ")
    board_tensor = transform_fen(board_str).type(torch.FloatTensor)
    assert board_tensor.size() == torch.Size([12, 8, 8])
    enpassant_tensor = en_passant_to_vec(enpassant_str).type(torch.FloatTensor)
    assert enpassant_tensor.size() == torch.Size([8,8])
    castling_tensor = castle_to_vec(castling_str).type(torch.FloatTensor)
    assert castling_tensor.size() == torch.Size([4])
    turn_tensor = torch.ByteTensor([TURN_TO_INT[turn_str]]).type(torch.FloatTensor)
    assert turn_tensor.size() == torch.Size([1])
    output_tensor = torch.cat((board_tensor.flatten(), enpassant_tensor.flatten(),castling_tensor.flatten(),turn_tensor.flatten()), 0)

    return output_tensor

def convert_move(move, spacing=1):
    if(isinstance(move, float) and np.isnan(move)):
        return 0
    else:
        end = move[4:].replace("q","11").replace("r","12").replace("b","13").replace("n","14")
        if(end == ""):
            end = "10"
        return int(
                move[:4].replace("a","1").replace("b","2").replace("c","3").replace("d","4").replace("e","5").replace("f","6").replace("g","7").replace("h","8")
                + end
            ) * spacing
print("Chargement du CSV...")
# Chargement des données à partir du fichier CSV
data = pd.read_csv("api/tactic_evals.csv")
print("CSV chargé.")

# Convertion des UCI-format moves en indices de classe
unique_moves = data["Move"].unique()
move_to_index = {move: i for i, move in enumerate(unique_moves)}
data["MoveIndex"] = data["Move"].map(move_to_index)


# Définitions d'un modèle de réseau neuronal pour la classification
class ChessClassificationNet(nn.Module):
    def __init__(self, num_classes):
        super(ChessClassificationNet, self).__init__()
        self.fc1 = nn.Linear(12 * 8 * 8 + 8 * 8 + 4 + 1, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, num_classes) 

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x) 
        return x

def create_classification_model(num_classes, input_size):
    model = ChessClassificationNet(num_classes)  
    checkpoint = torch.load("api/classification_model.pth") 
    return model



def predict_next_move(fen_str):
    num_classes = len(unique_moves)  
    input_size = 12 * 8 * 8 + 8 * 8 + 4 + 1  
    model = create_classification_model(num_classes, input_size)
    model.eval()  
    input_tensor = encode_fen_flat(fen_str).unsqueeze(0)

    board = chess.Board(fen_str)

    possible_moves = list(board.legal_moves)
    possible_moves = [move.uci() for move in possible_moves]


    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.softmax(output, dim=1)[0]
        sorted_indices = torch.argsort(probabilities, descending=True)
        sorted_moves = [unique_moves[idx] for idx in sorted_indices]

    legal_sorted_moves = [move for move in sorted_moves if move in possible_moves]

    return legal_sorted_moves[0]