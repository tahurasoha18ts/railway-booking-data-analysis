-- Passenger count per train
SELECT T.Train_Name, COUNT(*) AS passenger_count
FROM Train T
JOIN booked B ON T.Train_Number = B.Train_Number
GROUP BY T.Train_Name;

-- Bookings by date
SELECT B.Passanger_ssn, B.Status
FROM Train T
JOIN Train_status S ON T.Train_Name = S.TrainName
JOIN booked B ON B.Train_Number = T.Train_Number
WHERE S.TrainDate = 'YYYY-MM-DD';

-- Passengers by age range
SELECT B.Train_Number, P.first_name, T.Train_Name,
       T.Source_Station, T.Destination_Station,
       P.address, B.Ticket_Type, B.Status
FROM Passenger P
JOIN booked B ON P.SSN = B.Passanger_ssn
JOIN Train T ON T.Train_Number = B.Train_Number
WHERE (strftime('%Y','now') - strftime('%Y', P.bdate))
BETWEEN 20 AND 60;

-- Confirmed passengers by train
SELECT P.first_name, T.Train_Name, B.Train_Number, B.Status
FROM Train T
JOIN booked B ON T.Train_Number = B.Train_Number
JOIN Passenger P ON P.SSN = B.Passanger_ssn
WHERE B.Status = 'Booked'
AND T.Train_Name = 'Train Name';
