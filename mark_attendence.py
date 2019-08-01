
def mark(id,cat):
    import os
    import openpyxl as xl
    from datetime import datetime

    current_month,current_date=datetime.now().month,datetime.now().day
    book=xl.load_workbook(os.path.join("Database",cat,"Attendence.xlsx"))
    months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    month=months[current_month-1]
    sheet=book[month]
    row=1
    value_=sheet['A1'].value
    while(value_ != None):
        if(value_==id):
            sheet.cell(row=row,column=current_date+2).value="P"
            book.save(os.path.join("Database",cat,"Attendence.xlsx"))
            return True
        row+=1
        value_=sheet['A{0}'.format(row)].value
    book.save(os.path.join("Database",cat,"Attendence.xlsx"))
    return False


if __name__=="__main__":
    mark()
