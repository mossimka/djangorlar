from decouple import config

# -----------------------------------------------------------------
# variables
ENV_POSSIBLE_VALUES = [
  'dev', 
  'prod',
]
ENV_ID = config('ENV_ID', default='dev', cast=str)

SECRET_KEY = 'django-insecure-5+dtga7nlqs5rmeekvc^s*f+%1g5bs%3b%+83x#-91aomwd&_v'
