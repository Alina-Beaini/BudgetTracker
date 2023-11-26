from project import check_number_isvalid, check_yes_no, check_day


def test_check_number_isvalid():
    assert check_number_isvalid("twenty") == False
    assert check_number_isvalid("$10") == False
    assert check_number_isvalid("2/3") == False
    assert check_number_isvalid("-20") == False
    assert check_number_isvalid("0") == False
    assert check_number_isvalid("20!") == False

    assert check_number_isvalid("20") == True
    assert check_number_isvalid("20.504") == True

def test_check_yes_no():
    assert check_yes_no("yes") == True
    assert check_yes_no("y") == True
    assert check_yes_no("YeS") == True
    assert check_yes_no("No") == True
    assert check_yes_no("N") == True

    assert check_yes_no("nope") == False
    assert check_yes_no("132") == False
    assert check_yes_no("nooo") == False

def test_check_day():
    assert check_day("1") == True
    assert check_day("01") == True
    assert check_day("31") == True
    assert check_day("14") == True

    assert check_day("1.0") == False
    assert check_day("32") == False    
    assert check_day("0") == False
    assert check_day("twenty") == False
    assert check_day("-1") == False
    assert check_day("31/2") == False






