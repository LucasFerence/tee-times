# tee-times
Snags tee times from local MCG courses

`-u` : Username [REQUIRED]

`-p` : Password [REQUIRED]

`-course` : Course to play [REQUIRED] See valid values below

`-count` : Number of players [REQUIRED]

`-adv` : Days in advance to book (curr day + `adv`). Defaults to 7

`-start` : Earliest tee time barrier. Will not select a tee time before provided value. Ensure it is formatted correctly to the example. Example: `8:30 AM`. Defaults to `6:30 AM`

`-end` : Latest tee time barrier. Will not select a tee time after provided value. Ensure it is formatted correctly to the example. Example: `3:00 PM`. Defaults to `8:00 PM`

`--checkout` : If provided, will fully reserve the tee time

`--headless` : If provided, will not render a browser. Useful for running without a display

# Crontab scheduling

Link to help generate a cron tab https://crontab.guru

Example: cron tab to generate 6am on Saturday: `0 6 * * SAT`

Add crontabs to system:
Reference: https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx/

Open crontab: `crontab -e`

Add crontab to file on a new line

List crontab: `crontab -l`

Remove all cron jobs: `crontab -r`

I would recommend adding a log output file so you can track the output of the script.
Here is an example cron job:

`0 9 * * SAT ~/Scripts/tee-times.sh >> ~/Scripts/logs/tee-times`

# Script

To run the script, copy the script from `example-script.sh` into another directory, like `~/Scripts/` for example. Store it in a file called `tee-times.sh`

Run `chmod +x tee-times.sh` to make your script executable.

# Course values:
- FALLS_ROAD
- HAMPSHIRE_GREENS
- LAYTONSVILLE
- LITTLE_BENNET
- NEEDWOOD
- NORTHWEST
- POOLESVILLE
- RATTLEWOOD
