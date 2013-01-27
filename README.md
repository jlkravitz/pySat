pySat
=====

Retrieves vocabulary words from the SAT question of the day. 
Since the 'Sentence Completion' category is the only category 
with vocab word answers, new words will not be retrieved every day.

The only dependency is [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/).

To run once:

    python sat-vocab.py

To run automatically each day, open the user crontab file on the command line.

    $ crontab -e

Then, type the cron command at the bottom of the file.

    @daily /path/to/sat-vocab.py

You can also log the output of the script each time it's run.

    @daily /path/to/sat-vocab.py >> /path/to/your/log/file
