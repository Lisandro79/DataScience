# Example taken from https://medium.com/jbennetcodes/how-to-rewrite-your-sql-queries-in-pandas-and-more-149d341fc53e

import pandas as pd

airports = pd.read_csv('data/airports.csv')
airports_freq = pd.read_csv('data/airport-frequencies.csv')
runways = pd.read_csv('./data/runways.csv')

# |                      SQL                     |                 Pandas                |
# |:--------------------------------------------:|:-------------------------------------:|
# | select * from airports                       |                            |
# | select * from airports limit 3               |                     |
# | select id from airports where ident = 'KLAX' |              |
# | select distinct type from airport            |           |


# SELECT with multiple conditions
# select * from airports where iso_region = 'US-CA' and type = 'seaplane_base'
airports[(airports.iso_region == 'US-CA') & (airports.type == 'seaplane_base')]  # careful with Parenthesis

# select ident, name, municipality from airports where iso_region = 'US-CA' and type = 'large_airport'
airports[(airports.iso_region == 'US-CA') & (airports.type == 'large_airport')][['ident', 'name', 'municipality']]

# ORDER BY
# select * from airport_freq where airport_ident = 'KLAX' order by type
airports_freq[airports_freq.airport_ident == 'KLAX'].sort_values('type')

# select * from airport_freq where airport_ident = 'KLAX' order by type desc
airports_freq[airports_freq.airport_ident == 'KLAX'].sort_values('type', ascending=False)


# IN... NOT IN
# select * from airports where type in ('heliport', 'balloonport')
airports[airports.type.isin(['heliport', 'baloonport'])]
# select * from airports where type not in ('heliport', 'balloonport')
airports[~airports.type.isin(['heliport', 'baloonport'])]


# GROUP BY
# select iso_country, type, count(*) from airports group by iso_country, type order by iso_country, type

# select iso_country, type, count(*) from airports group by iso_country, type order by iso_country, count(*) desc


