import streamlit as st
import sqlite3 as sq
import pandas as pd

conn = sq.connect("railways.db")


cur = conn.cursor()

def get_booked_trains(lname, fname):
    sql = '''select Train_Number
            from Passenger join Booked on SSN = Passanger_ssn
            where first_name = "''' + fname + '" and ' + "last_name ='" + lname + "';"
    data = pd.read_sql_query(sql, conn)
    return data
    # res = cur.execute(sql)
    # return res


def get_booked_from_date(date):
    sql = '''SELECT B.Passanger_ssn, B.Status
    from (Train T JOIN Train_status S ON T.Train_Name = S.TrainName)  JOIN booked B ON B.Train_Number = T.Train_Number
    WHERE S.TrainDate = '{}';'''.format(date)
    res = pd.read_sql_query(sql, conn)
    return res


def get_passengers_wrt_age(fage, lage):
    sql = '''SELECT  B.Train_Number,P.first_name, T.Train_Name, T.Source_Station, T.Destination_Station,P.address, B.Ticket_Type, B.Status
                FROM Passenger P 
                JOIN booked B ON P.SSN = B.Passanger_ssn 
                JOIN Train T ON T.Train_Number = B.Train_Number
                WHERE strftime('%Y','now')- strftime('%Y',strftime(P.bdate)) BETWEEN {} AND {};
    '''.format(fage, lage)
    res = pd.read_sql_query(sql, conn)
    return res


def get_agg_train_count_passengers():
    sql = '''SELECT T.Train_Name, count(*) as count
    FROM Train T JOIN booked B ON T.Train_Number = B.Train_Number
    GROUP by T.Train_Name
    '''
    res = pd.read_sql_query(sql, conn)
    return res


def get_passengers_from_train_name(train_name):
    sql = '''SELECT P.first_name, T.Train_Name, B.Train_Number, B.Status
    FROM Train T JOIN booked B ON T.Train_Number = B.Train_Number 
    JOIN Passenger P ON P.SSN = B.Passanger_ssn
    WHERE B.Status = 'Booked' AND T.Train_Name = "{}";'''.format(train_name)
    res = pd.read_sql_query(sql, conn)
    return res


def cancel_ticket(ssn, tno):
    sql = ''' DELETE FROM booked WHERE Passanger_ssn = "{}" AND Train_Number = "{}";'''.format(ssn, tno)

    cur.execute(sql)


def main():

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Railways Data", "Booking Date", "Train Information", "Passenger Count", "Confirmed Status", "Cancel Ticket"])

    with tab1:
        st.title("Trains booked by:")
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")

        if(st.button("Submit", type="primary")):
            data= get_booked_trains(lname,fname)
            st.table(data=data)

    with tab2:
        st.header("Enter the date to get the confirmed ticket list")
        date = st.text_input("Date")
        if(st.button("Submit1", type="primary")):
            data= get_booked_from_date(date)
            st.table(data=data)

    with tab3:
        st.header("Train and Passenger information with respect to date")
        min_age = st.number_input("Minimum Age", min_value=0, max_value=150, step=1, value=10)
        max_age = st.number_input("Maximum Age", min_value=0, max_value=150, step=1, value=80)
        

        if st.button("Submit2", type="primary"):
            data = get_passengers_wrt_age(min_age, max_age)
            st.table(data=data)

    with tab4:
        st.header("Trains along with passenger count in it:")
        data = get_agg_train_count_passengers()
        st.table(data = data)

    with tab5:
        st.header("Enter Train name to know the confirmed status:")
        train_name = st.text_input("Train Name")
        data = get_passengers_from_train_name(train_name)
        st.table(data = data)
        

    with tab6:
        st.header("Cancel Ticket:")
        ssn = st.text_input("SSN")
        tno = st.text_input("TNO")

        if st.button("Submit3", type="primary"):
            
            cancel_ticket(ssn, tno)
            st.success("Deleted")
    # with tab6:
    #     st.header("Cancel Ticket")
    #     ssn = st.text_input("SSN")
    #     tno = st.text_input("TNO")

    # if st.button("Submit3", type="primary"):
    #     # Call cancel_ticket function
    #     result = cancel_ticket(ssn, tno)
        
    #     # Display appropriate success message
    #     if result:
    #         st.success("Ticket canceled and next passenger from waiting list confirmed.")
    #     else:
    #         st.success("Ticket canceled successfully, no passengers in waiting list.")



if __name__ == "__main__":
    main()