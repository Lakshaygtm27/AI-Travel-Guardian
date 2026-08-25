\copy destinations(city, state, country, safety_score, popularity_score, avg_budget) FROM 'database/destinations.csv' WITH (FORMAT csv, HEADER true);
\copy attractions(name, city, country, latitude, longitude, rating, cost) FROM 'database/attractions.csv' WITH (FORMAT csv, HEADER true);
\copy hospitals(name, city, country, latitude, longitude, phone) FROM 'database/hospitals.csv' WITH (FORMAT csv, HEADER true);
\copy emergency_contacts(country, police, ambulance, fire, tourism) FROM 'database/emergency_contacts.csv' WITH (FORMAT csv, HEADER true);
\copy scams(city, scam, severity) FROM 'database/scams.csv' WITH (FORMAT csv, HEADER true);
