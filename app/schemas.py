from pydantic import BaseModel, Field


class PredictionResults(BaseModel):
    prediction: int = Field(description="0 means False and 1 means True")
    probability: float = Field(description="Probability of True")


class InputSchema(BaseModel):
    # order of the features has to mach training
    mean_radius: float
    mean_texture: float
    mean_smoothness: float
    mean_compactness: float
    mean_concavity: float
    mean_concave_points: float
    mean_symmetry: float
    mean_fractal_dimension: float
    texture_error: float
    area_error: float
    smoothness_error: float
    compactness_error: float
    concavity_error: float
    symmetry_error: float
    fractal_dimension_error: float
    worst_texture: float
    worst_smoothness: float
    worst_compactness: float
    worst_symmetry: float
    worst_fractal_dimension: float


column_map = {
    "mean_radius": "mean radius",
    "mean_texture": "mean texture",
    "mean_smoothness": "mean smoothness",
    "mean_compactness": "mean compactness",
    "mean_concavity": "mean concavity",
    "mean_concave_points": "mean concave points",
    "mean_symmetry": "mean symmetry",
    "mean_fractal_dimension": "mean fractal dimension",
    "texture_error": "texture error",
    "area_error": "area error",
    "smoothness_error": "smoothness error",
    "compactness_error": "compactness error",
    "concavity_error": "concavity error",
    "symmetry_error": "symmetry error",
    "fractal_dimension_error": "fractal dimension error",
    "worst_texture": "worst texture",
    "worst_smoothness": "worst smoothness",
    "worst_compactness": "worst compactness",
    "worst_symmetry": "worst symmetry",
    "worst_fractal_dimension": "worst fractal dimension",
}
