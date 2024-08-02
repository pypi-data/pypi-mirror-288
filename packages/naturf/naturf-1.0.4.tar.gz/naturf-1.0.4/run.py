from importlib.resources import files
from naturf import driver

input_shapefile_path = str(files("naturf").joinpath("data").joinpath("C-5.shp"))

inputs = {"input_shapefile": input_shapefile_path}
outputs = ["write_binary", "write_index"]
model = driver.Model(inputs, outputs)

df = model.execute()
model.graph()
