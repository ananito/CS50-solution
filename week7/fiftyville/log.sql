-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Get the Crime scene report
SELECT description
FROM crime_scene_reports
WHERE year = 2021
	AND day = 28
	AND month = 7
	AND street = "Humphrey Street";

-- Read The interview transcript
SELECT name,
	transcript
FROM interviews
WHERE year = 2021
	AND day = 28
	AND month = 7;

-- GET all the people that was exiting the bakery within 10 min of the crime using their licence plate we found in the bakery security log
SELECT people.name
FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE bakery_security_logs.year = 2021
	AND bakery_security_logs.month = 7
	AND bakery_security_logs.day = 28
	AND bakery_security_logs.minute >= 15
	AND bakery_security_logs.minute < 25
	AND bakery_security_logs.activity = "exit";

-- Search the bank accout record for the bank account number
SELECT bank_accounts.account_number,
	people.*
FROM bank_accounts
JOIN people ON bank_accounts.person_id = people.id
WHERE people.id IN (
		SELECT people.id
		FROM people
		JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
		WHERE bakery_security_logs.year = 2021
			AND bakery_security_logs.month = 7
			AND bakery_security_logs.day = 28
			AND bakery_security_logs.minute >= 15
			AND bakery_security_logs.minute < 25
			AND bakery_security_logs.activity = "exit"
		);

-- Find the name of the people who took money at leggett Street
SELECT name
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2021
	AND atm_transactions.month = 7
	AND atm_transactions.day = 28
	AND atm_transactions.atm_location = 'Leggett Street'
	AND atm_transactions.transaction_type = 'withdraw';

-- Check the call records since the theif called someone for less than a minute
SELECT people.name AS "caller",
	people.phone_number
FROM people
JOIN phone_calls ON people.phone_number = phone_calls.CALLER
WHERE phone_calls.year = 2021
	AND phone_calls.month = 7
	AND phone_calls.day = 28
	AND phone_calls.duration < 60;

-- Find the name of the receivers
SELECT people.name AS "receiver",
	people.phone_number
FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.year = 2021
	AND phone_calls.month = 7
	AND phone_calls.day = 28
	AND phone_calls.duration < 60;

-- Search the flight record since the theif is leaving early in the morning
SELECT id
FROM flights
WHERE origin_airport_id = 8
	AND year = 2021
	AND month = 7
	AND day = 29
ORDER BY hour,
	minute;

-- Find the passport number of the people on the earliest flight
SELECT passport_number
FROM passengers
WHERE flight_id = (
		SELECT id
		FROM flights
		WHERE origin_airport_id = 8
			AND year = 2021
			AND month = 7
			AND day = 29
		ORDER BY hour,
			minute
		);

-- find the name of all the people on the flight
SELECT people.name
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passengers.passport_number IN (
		SELECT passport_number
		FROM passengers
		WHERE flight_id = (
				SELECT id
				FROM flights
				WHERE origin_airport_id = 8
					AND year = 2021
					AND month = 7
					AND day = 29
				ORDER BY hour,
					minute LIMIT(1)
				)
		);

-- Find The city the suspect is going to
SELECT city
FROM airports
WHERE id = (
		SELECT destination_airport_id
		FROM flights
		WHERE id = (
				SELECT flight_id
				FROM passengers
				WHERE id = 36
					AND passport_number = "5773159633"
				)
		);
