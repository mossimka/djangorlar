# project modules
from decouple import config

# -----------------------------------------------------------------
# variables
ENV_POSSIBLE_VALUES = [
  'dev', 
  'prod',
]
ENV_ID = config('ENV_ID', default='dev', cast=str)
SECRET_KEY = 'django-insecure-i^f%hjuqb*qfkd86ux-a1is@(%i!)!lr7znzten#6q0_488)4v'