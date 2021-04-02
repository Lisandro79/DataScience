# Connect your script to Neptune
import neptune
import os

token = os.environ.get('NEPTUNE_API_TOKEN')

neptune.init(project_qualified_name='saldinor/PilarScoring',
             api_token=token,
             )

# Create experiment
neptune.create_experiment()

# Log metrics to experiment
from time import sleep

neptune.log_metric('single_metric', 0.62)

for i in range(100):
    sleep(0.2)  # to see logging live
    neptune.log_metric('random_training_metric', i * 0.6)
    neptune.log_metric('other_random_training_metric', i * 0.4)
