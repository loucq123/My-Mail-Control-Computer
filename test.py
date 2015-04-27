import MCC


def testSearch_word():
    assert MCC.search_word(r'(abc)', 'fabc') == 'abc'
    assert MCC.search_word(r'(abc)', 'abcf') == 'abc'
    assert MCC.search_word(r'(abc)', 'fabcf') == 'abc'
    assert MCC.search_word(r'(abc)', 'abc') == 'abc'

    assert MCC.search_word(r'(a)', 'ba') == 'a'
    assert MCC.search_word(r'(a)', 'ab') == 'a'
    assert MCC.search_word(r'(a)', 'bab') == 'a'
    assert MCC.search_word(r'(a)', 'a') == 'a'

    assert MCC.search_word(r'a(b)c', 'fabc') == 'b'
    assert MCC.search_word(r'a(b)c', 'abcf') == 'b'
    assert MCC.search_word(r'a(b)c', 'fabcf') == 'b'
    assert MCC.search_word(r'a(b)c', 'abc') == 'b'

def testConfiguration():
    MCC.configuration()
    assert MCC.host == "pop3.163.com"
    assert MCC.username == "loucq123@163.com"
    assert MCC.password == "helloworld0205"
    assert MCC.bossEmail == "qigouge123@qq.com"
    assert MCC.timeLimit == 60

def testExtract_mail_time():
    s = 'Mon, 27 Apr 2015 08:30:49 +0800'
    testCase = ['Mon, 27 Apr 2015 08:30:49 +0800',
                'Mon, 09 Jan 2015 11:05:06 +0000',
                'Sun, 28 Feb 1999 00:00:00 +0800',
                'Sat, 31 Mar 1994 11:11:11 +8000',
                'Wed, 18 May 2010 22:22:22 +4000',
                'Tus, 22 Jun 2009 02:05:10 +8000',
                'Tur, 23 Jul 2008 15:15:00 +9000',
                'Fri, 24 Aug 2007 16:16:16 +6000',
                'Mon, 25 Sep 2006 17:00:09 +5000',
                'Mon, 26 Oct 2005 18:09:00 +4000',
                'Wed, 27 Nov 2004 00:19:04 +9999',
                'Sat, 28 Dec 2003 04:12:34 +9999'
               ]
    testAnswer = [[2015, 4, 27, 8, 30],
                  [2015, 1, 9, 11, 5],
                  [1999, 2, 28, 0, 0],
                  [1994, 3, 31, 11, 11],
                  [2010, 5, 18, 22, 22],
                  [2009, 6, 22, 2, 5],
                  [2008, 7, 23, 15, 15],
                  [2007, 8, 24, 16, 16],
                  [2006, 9, 25, 17, 0],
                  [2005, 10, 26, 18, 9],
                  [2004, 11, 27, 0, 19],
                  [2003, 12, 28, 4, 12]
                 ]
    for caseIndex in range(len(testCase)):
        assert MCC.extract_mail_time(testCase[caseIndex]) == testAnswer[caseIndex]

def testIs_leapyear():
    assert MCC.is_leapyear(2000) == True
    assert MCC.is_leapyear(2004) == True
    assert MCC.is_leapyear(1900) == False
    assert MCC.is_leapyear(100) == False
    assert MCC.is_leapyear(400) == True

def testChange_time_into_minutes():
	
    assert MCC.change_time_into_minutes([1, 1, 1, 0, 0]) == 0

    assert MCC.change_time_into_minutes([1, 1, 1, 0, 59]) == 59
    assert MCC.change_time_into_minutes([1, 1, 1, 1, 0]) == 1*60
    assert MCC.change_time_into_minutes([1, 1, 1, 1, 4]) == 1*60 + 4
    assert MCC.change_time_into_minutes([1, 1, 1, 2, 0]) == 2*60
    assert MCC.change_time_into_minutes([1, 1, 1, 2, 7]) == 2*60 + 7

    assert MCC.change_time_into_minutes([1, 1, 1, 0, 0]) == (1-1)*24*60
    assert MCC.change_time_into_minutes([1, 1, 1, 1, 0]) == (1-1)*24*60 + 1*60
    assert MCC.change_time_into_minutes([1, 1, 1, 1, 1]) == (1-1)*24*60 + 1*60 + 1
    assert MCC.change_time_into_minutes([1, 1, 1, 0, 1]) == (1-1)*24*60 + 1
    assert MCC.change_time_into_minutes([1, 1, 2, 4, 6]) == (2-1)*24*60 + 4*60 + 6

    assert MCC.change_time_into_minutes([1, 2, 1, 0, 0]) == 31*24*60
    assert MCC.change_time_into_minutes([1, 2, 2, 0, 0]) == (31+1)*24*60
    assert MCC.change_time_into_minutes([1, 2, 2, 2, 1]) == (31+1)*24*60 + 2*60 +1
    assert MCC.change_time_into_minutes([1, 3, 1, 0, 0]) == (31+28)*24*60
    assert MCC.change_time_into_minutes([1, 4, 1, 0, 0]) == (31+28+31)*24*60
    assert MCC.change_time_into_minutes([1, 5, 1, 0, 0]) == (31+28+31+30)*24*60
    assert MCC.change_time_into_minutes([1, 6, 1, 0, 0]) == (31+28+31+30+31)*24*60
    assert MCC.change_time_into_minutes([1, 7, 1, 0, 0]) == (31+28+31+30+31+30)*24*60
    assert MCC.change_time_into_minutes([1, 8, 1, 0, 0]) == (31+28+31+30+31+30+31)*24*60
    assert MCC.change_time_into_minutes([1, 9, 1, 0, 0]) == (31+28+31+30+31+30+31+31)*24*60
    assert MCC.change_time_into_minutes([1, 10, 1, 0, 0]) == (31+28+31+30+31+30+31+31+30)*24*60
    assert MCC.change_time_into_minutes([1, 11, 1, 0, 0]) == (31+28+31+30+31+30+31+31+30+31)*24*60
    assert MCC.change_time_into_minutes([1, 12, 1, 0, 0]) == (31+28+31+30+31+30+31+31+30+31+30)*24*60

    assert MCC.change_time_into_minutes([2, 1, 1, 0, 0]) == 365*24*60
    assert MCC.change_time_into_minutes([2, 2, 1, 0, 0]) == 365*24*60 + 31*24*60
    assert MCC.change_time_into_minutes([2, 2, 2, 0, 0]) == 365*24*60 + 32*24*60
    assert MCC.change_time_into_minutes([2, 2, 2, 4, 59]) == 365*24*60 + 32*24*60 + 4*60 +59

    assert MCC.change_time_into_minutes([4, 2, 1, 0, 0]) == (4-1)*365*24*60 + 31*24*60 
    assert MCC.change_time_into_minutes([4, 3, 1, 0, 0]) == (4-1)*365*24*60 + (31+29)*24*60
    assert MCC.change_time_into_minutes([4, 3, 1, 5, 4]) == (4-1)*365*24*60 + (31+29)*24*60 + 5*60 + 4

    assert MCC.change_time_into_minutes([100, 1, 1, 0, 0]) == 24*366*24*60 + (100-24-1)*365*24*60
    assert MCC.change_time_into_minutes([100, 3, 1, 1, 1]) == 24*366*24*60 + (100-24-1)*365*24*60 + (31+28)*24*60 + 61
    assert MCC.change_time_into_minutes([101, 1, 1, 0, 0]) == 24*366*24*60 + (100-24)*365*24*60
    assert MCC.change_time_into_minutes([101, 3, 1, 1, 1]) == 24*366*24*60 + (100-24)*365*24*60 + (31+28)*24*60 + 61

    assert MCC.change_time_into_minutes([400, 1, 1, 0, 0]) == 96*366*24*60 + (400-97)*365*24*60
    assert MCC.change_time_into_minutes([400, 3, 1, 5, 4]) == 96*366*24*60 + (400-97)*365*24*60 + (31+29)*24*60 + 5*60 + 4
    assert MCC.change_time_into_minutes([401, 1, 1, 0, 0]) == 97*366*24*60 + (400-97)*365*24*60
    assert MCC.change_time_into_minutes([401, 3, 1, 5, 4]) == 97*366*24*60 + (400-97)*365*24*60 + (31+28)*24*60 + 5*60 + 4

    assert MCC.change_time_into_minutes([2015, 4, 27, 20, 26]) == 5*(97*366*24*60 + (400-97)*365*24*60) + \
                                                                  3*(366*24*60 + 3*365*24*60) + \
                                                                  2*(365*24*60) + \
                                                                  (31+28+31)*24*60 + \
                                                                  26*24*60 + 20*60 + 26 

def testIs_numbers_in_precision():
    assert MCC.is_numbers_in_precision(1, 0, 1) == True
    assert MCC.is_numbers_in_precision(99, 0, 1) == False
    assert MCC.is_numbers_in_precision(100, 100, 0) == True

    assert MCC.is_numbers_in_precision(1.0, 0.0, 1.0) == True
    assert MCC.is_numbers_in_precision(99.0, 1.0, 1.0) == False
    assert MCC.is_numbers_in_precision(4.0, 4.0, 0.0) == True

    assert MCC.is_numbers_in_precision(1.0, 0, 1) == True
    assert MCC.is_numbers_in_precision(99.0, 0, 1) == False
    assert MCC.is_numbers_in_precision(99.0, 99, 1) == True

    assert MCC.is_numbers_in_precision(1, 0, 1.0) == True
    assert MCC.is_numbers_in_precision(99, 0, 1.0) == False
    assert MCC.is_numbers_in_precision(99, 99, 0.0) == True

    assert MCC.is_numbers_in_precision(1, 0.0, 1.0) == True
    assert MCC.is_numbers_in_precision(99, 0.0, 1.0) == False
    assert MCC.is_numbers_in_precision(99, 99.0, 1.0) == True

    assert MCC.is_numbers_in_precision(1059428670, 1059429439, 5) == False

def test():
    testSearch_word()
    testConfiguration()
    testExtract_mail_time()
    testIs_leapyear()
    testChange_time_into_minutes()
    testIs_numbers_in_precision()
    print "tests pass"


if __name__ == '__main__':
    test()