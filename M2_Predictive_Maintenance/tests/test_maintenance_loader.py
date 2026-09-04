from src.maintenance_data_loader import MaintenanceDataLoader


data_path = "data/raw/ai4i2020.csv"


loader = MaintenanceDataLoader(
    data_path
)


df = loader.load_data()


print("\nFirst 5 rows:")
print(df.head())


print("\nDataset Shape:")
print(df.shape)


print("\nColumns:")
print(df.columns.tolist())


# Test a specific machine/product
product_id = df["Product ID"].iloc[0]

machine_data = loader.get_machine_data(
    df,
    product_id
)


print(
    f"\nData for Product ID: {product_id}"
)

print(machine_data)