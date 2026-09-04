from src.data_loader import DataLoader


DATA_PATH = "data/processed/energy_agent_dataset.csv"


loader = DataLoader(DATA_PATH)

df = loader.load_data()


print("\nFirst 5 rows:")
print(df.head())


print("\nDataset shape:")
print(df.shape)


print("\nColumns:")
print(df.columns.tolist())