import sqlite3

sqlite_file = 'crowd_ahp.sqlite'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn='goals', nf='goal', ft='TEXT'))

c.execute('CREATE TABLE criteria (goal_id INTEGER, criteria_id INTEGER, criteria TEXT, PRIMARY KEY (goal_id, criteria_id))')

c.execute('CREATE TABLE "criteria_comparisons" ("goal_id" INTEGER NOT NULL ,"criteria_1_id" INTEGER NOT NULL ,"criteria_2_id" INTEGER NOT NULL ,"value" REAL NOT NULL )')

c.execute('CREATE TABLE alternatives (alternative_id INTEGER, goal_id INTEGER, alternative TEXT, PRIMARY KEY (alternative_id, goal_id))')

c.execute('CREATE TABLE "criteria_comparisons" ("goal_id" INTEGER NOT NULL ,"criteria_1_id" INTEGER NOT NULL ,"criteria_2_id" INTEGER NOT NULL ,"value" REAL NOT NULL )')

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()