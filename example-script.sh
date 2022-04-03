# Example script to run this, can be provided to a cron job to run with pre-configured arguments
# --checkout not included in example, but is needed if you wish to actually reserve a tee time

# This example will book a tee time at needwood for 2 at the earliest time in 7 days from the time it was ran.
# It will only select a tee time after 8:30 AM
python3 ~/{your-dir}/tee-times/tee-times.py -u '{username}' -p '{password}' -course NEEDWOOD -count 2 -start '8:30 AM'