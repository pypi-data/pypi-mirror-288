import numpy as np
import torch
import torch.nn.functional as F
from data_loaders import load_data_labels_based_on_dataset
from data_utils import get_dataset_basic_info, get_input_data_path, standard_saving_path
from DiffE.diffE_models import Decoder, DiffE, Encoder, LinearClassifier
from DiffE.diffE_utils import EEGDataset
from share import ROOT_VOTING_SYSTEM_PATH, datasets_basic_infos
from sklearn.metrics import top_k_accuracy_score
from torch.utils.data import DataLoader

dataset_name = "aguilera_traditional"  # Only two things I should be able to change

data_path: str = get_input_data_path(dataset_name)
dataset_info: dict = get_dataset_basic_info(datasets_basic_infos, dataset_name)


def diffE_evaluation(subject_id: int, X, Y, dataset_info, device: str = "cuda:0"):

    X = X[
        :, :, : -1 * (X.shape[2] % 8)
    ]  # 2^3=8 because there are 3 downs and ups halves.
    # Dataloader
    batch_size2 = 260
    train_loader = DataLoader(EEGDataset(X, Y), batch_size=batch_size2, shuffle=False)

    ddpm_dim = 128
    encoder_dim = 256
    fc_dim = 512
    # Define model
    model_path: str = standard_saving_path(
        dataset_info, "DiffE", "", file_ending="pt", subject_id=subject_id
    )
    num_classes = dataset_info["#_class"]
    channels = dataset_info["#_channels"]

    encoder = Encoder(in_channels=channels, dim=encoder_dim).to(device)
    decoder = Decoder(
        in_channels=channels, n_feat=ddpm_dim, encoder_dim=encoder_dim
    ).to(device)
    fc = LinearClassifier(encoder_dim, fc_dim, emb_dim=num_classes).to(device)
    diffe = DiffE(encoder, decoder, fc).to(device)

    # load the pre-trained model from the file
    diffe.load_state_dict(torch.load(model_path))

    diffe.eval()

    with torch.no_grad():
        Y = []
        Y_hat = []
        for x, y in train_loader:
            x, y = x.to(device).float(), y.type(torch.LongTensor).to(device)
            encoder_out = diffe.encoder(x)
            y_hat = diffe.fc(encoder_out[1])
            y_hat = F.softmax(y_hat, dim=1)

            Y.append(y.detach().cpu())
            Y_hat.append(y_hat.detach().cpu())

        # List of tensors to tensor to numpy
        Y = torch.cat(Y, dim=0).numpy()  # (N, )
        Y_hat = torch.cat(Y_hat, dim=0).numpy()  # (N, 13): has to sum to 1 for each row

        return Y, Y_hat


if __name__ == "__main__":
    print(f"CUDA is available? {torch.cuda.is_available()}")

    dataset_name = "aguilera_traditional"  # Only two things I should be able to change

    # Folders and paths
    dataset_foldername = dataset_name + "_dataset"
    computer_root_path = ROOT_VOTING_SYSTEM_PATH + "/Datasets/"
    data_path = computer_root_path + dataset_foldername
    print(data_path)
    dataset_info = datasets_basic_infos[dataset_name]
    all_subjects_accuracy: list = []

    for subject_id in range(1, dataset_info["subjects"] + 1):
        print(f"\nSubject: {subject_id}")
        _, X, Y = load_data_labels_based_on_dataset(dataset_info, subject_id, data_path)

        # create an argument parser for the data loader path

        Y_returned, Y_hat = diffE_evaluation(
            subject_id=subject_id, X=X, Y=Y, dataset_info=dataset_info
        )

        # Accuracy and Confusion Matrix
        accuracy = top_k_accuracy_score(
            Y_returned, Y_hat, k=1, labels=np.arange(0, dataset_info["#_class"])
        )
        all_subjects_accuracy.append(accuracy)
        print(f"Test accuracy: {accuracy:.2f}%")
    print(f"Test accuracy: {all_subjects_accuracy}")
