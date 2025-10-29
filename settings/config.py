from decouple import config

# -----------------------------------------------------------------
# variables
ENV_POSSIBLE_VALUES = [
  'dev', 
  'prod',
]
ENV_ID = config('ENV_ID', default='dev', cast=str)

SECRET_KEY = config('SECRET_KEY', cast=str)
