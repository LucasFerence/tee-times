# tee-times
Snags tee times from local MCG courses

`-u` : Username [REQUIRED]

`-p` : Password [REQUIRED]

`-count` : Number of players [REQUIRED]

# Crontab scheduling

Link to help generate a cron tab https://crontab.guru

Example: cron tab to generate 6am on Saturday: `0 6 * * SAT`

Add crontabs to system:
Reference: https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx/

Open crontab: `crontab -e`

Add crontab to file on a new line

List crontab: `crontab -l`

Remove all cron jobs: `crontab -r`
