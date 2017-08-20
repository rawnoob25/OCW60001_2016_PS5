"""
This assignment uses many important techniques. 

Use of the __repr__() instance method and eval() function are demonstrated.
There's also use of date formatting functions.

This assignment makes extensive use of inheritance.

The code provided to students in this assignment included code to read data
from the internet and to display data on a TKinter GUI. My GUI code doesn't work. This
can be confirmed by calling the test_full_application() function. The error
message thrown by Python is 
"RecursionError: maximum recursion depth exceeded while calling a Python object"

 
Even though my GUI code doesn't work, all of the teaching staff unit tests (in ps5_test.py) pass. I'm also
able to successfully read the provided Trigger configuration file ("triggers.txt").
This is tested by the test method test_read_config_file(). There are other associated
tests contained inside this file for each of the concrete Trigger subclasses.

The __str__() instance methods of the AndTrigger and OrTrigger classes 
don't return the expected string.

"""

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re
from datetime import timedelta


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate
#======================
# Triggers
#======================

class Trigger(object):
    
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError
    
    
        
#%%
#def is_subListOf(l1, l2):
#        """
#        This is a static method (function) for testing.
#        
#        Returns true if and only if the sequence of elements in l1
#        appears in l2
#        """
#        if len(l2)<len(l1):
#            return False
#        n = len(l2)
#        m = len(l1)
#        for i in range(m, n):
#            if l2[i-m:i] == l1:
#                return True
#        return False
#
#l1 = "the cow jumps".split()
#l2 = "moon bottle the cow the the cow jumps over yonder".split()
#print(l1)
#print(l2)
#print(is_subListOf(l1,l2))
#print(is_subListOf(l2,l1))
#%%
# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    
    def __str__(self):
        return self.phrase
    
    @staticmethod
    def is_subListOf(l1,l2):
        """
        Returns true if and only if the sequence of elements in l1
        appears in l2
        """
        if len(l2)<len(l1):
            return False
        n = len(l2)
        m = len(l1)
        
        if m==n:
            return l1 == l2
        for i in range(m, n+1):
            if l2[i-m:i] == l1:
                return True
        return False
    
    def is_phrase_in(self, text):
        words = [word.lower() for word in re.findall(r"[\w]+", text)]
        phraseWords = self.phrase.split()
        return PhraseTrigger.is_subListOf(phraseWords, words)
    
        
# def test1TitleTrigger(self):
#        cuddly    = NewsStory('', 'The purple cow is soft and cuddly.', '', '', datetime.now())
#        exclaim   = NewsStory('', 'Purple!!! Cow!!!', '', '', datetime.now())
#        symbols   = NewsStory('', 'purple@#$%cow', '', '', datetime.now())
#        spaces    = NewsStory('', 'Did you see a purple     cow?', '', '', datetime.now())
#        caps      = NewsStory('', 'The farmer owns a really PURPLE cow.', '', '', datetime.now())
#        exact     = NewsStory('', 'purple cow', '', '', datetime.now())
#
#        plural    = NewsStory('', 'Purple cows are cool!', '', '', datetime.now())
#        separate  = NewsStory('', 'The purple blob over there is a cow.', '', '', datetime.now())
#        brown     = NewsStory('', 'How now brown cow.', '' ,'', datetime.now())
#        badorder  = NewsStory('', 'Cow!!! Purple!!!', '', '', datetime.now())
#        nospaces  = NewsStory('', 'purplecowpurplecowpurplecow', '', '', datetime.now())
#        nothing   = NewsStory('', 'I like poison dart frogs.', '', '', datetime.now())
#
#        s1 = TitleTrigger('PURPLE COW')
#        s2  = TitleTrigger('purple cow')
#        for trig in [s1, s2]:
#            self.assertTrue(trig.evaluate(cuddly), "TitleTrigger failed to fire when the phrase appeared in the title.")
#            self.assertTrue(trig.evaluate(exclaim), "TitleTrigger failed to fire when the words were separated by exclamation marks.")
#            self.assertTrue(trig.evaluate(symbols), "TitleTrigger failed to fire when the words were separated by assorted punctuation.")
#            self.assertTrue(trig.evaluate(spaces), "TitleTrigger failed to fire when the words were separated by multiple spaces.")
#            self.assertTrue(trig.evaluate(caps), "TitleTrigger failed to fire when the phrase appeared with both uppercase and lowercase letters.")
#            self.assertTrue(trig.evaluate(exact), "TitleTrigger failed to fire when the words in the phrase were the only words in the title.")
#            
#            self.assertFalse(trig.evaluate(plural), "TitleTrigger fired when the words in the phrase were contained within other words.")
#            self.assertFalse(trig.evaluate(separate), "TitleTrigger fired when the words in the phrase were separated by other words.")
#            self.assertFalse(trig.evaluate(brown), "TitleTrigger fired when only part of the phrase was found.")
#            self.assertFalse(trig.evaluate(badorder), "TitleTrigger fired when the words in the phrase appeared out of order.")
#            self.assertFalse(trig.evaluate(nospaces), "TitleTrigger fired when words were not separated by spaces or punctuation.")
#            self.assertFalse(trig.evaluate(nothing), "TitleTrigger fired when none of the words in the phrase appeared.")        

def sep():
    print("---------------")
def testTitleTrigger():
    cuddly    = NewsStory('', 'The purple cow is soft and cuddly.', '', '', datetime.now())
    exclaim   = NewsStory('', 'Purple!!! Cow!!!', '', '', datetime.now())
    symbols   = NewsStory('', 'purple@#$%cow', '', '', datetime.now())
    spaces    = NewsStory('', 'Did you see a purple     cow?', '', '', datetime.now())
    s1 = TitleTrigger('PURPLE COW')
    s2  = TitleTrigger('purple cow')
    def evalString(trigger, story):
        part0 = "Evaluating trigger '"
        part1 = trigger.__str__()
        part2 = "' with story title '"
        part3 = story.get_title()
        part4 = "':"
        return part0+part1+part2+part3+part4
    for trig in [s1, s2]:
        print(evalString(trig, cuddly)+str(trig.evaluate(cuddly)))
        sep()
        print(evalString(trig, exclaim)+str(trig.evaluate(exclaim)))
        sep()
        print(evalString(trig, symbols)+str(trig.evaluate(symbols)))
        sep()
        print(evalString(trig, spaces)+str(trig.evaluate(spaces)))
        sep()
# Problem 3
# TODO: TitleTrigger




class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super(TitleTrigger, self).__init__(phrase)
        
    def evaluate(self, story):
        """
        Returns True if and only if the Trigger phrase is contained in the title
        of the story.
        
        Parameters: story, a NewStory instance
        """
        title = story.get_title()
        return self.is_phrase_in(title)
        
    def __repr__(self):
        return "TitleTrigger('"+self.phrase+"')"
    
    def __str__(self):
        return "Triggered by titles matching: "+self.phrase

    def __eq__(self, another):
        return isinstance(another, TitleTrigger) and self.phrase == another.phrase

def test_TitleTrigger():
    t = TitleTrigger("George Bush")
    print(t)
    theRepr = t.__repr__()
    print(theRepr)
    copy = eval(theRepr)
    print(copy)
    assert t == copy
    assert copy == t
        

        
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super(DescriptionTrigger, self).__init__(phrase)
    
    def evaluate(self, story):
        description = story.get_description()
        return self.is_phrase_in(description)
    
    def __repr__(self):
        return "DescriptionTrigger('"+self.phrase+"')"
    
    def __str__(self):
        return "Triggered by descriptions matching: "+self.phrase
    
    def __eq__(self, another):
        return isinstance(another, DescriptionTrigger) and self.phrase == another.phrase
    
def test_DescriptionTrigger():
    d = DescriptionTrigger("Mohandas Gandhi")
    print(d)
    theRepr = d.__repr__()
    print(theRepr)
    copy = eval(theRepr)
    print(copy)
    assert d == copy
    assert copy == d
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, timeString):
        fmt = "%d %b %Y %H:%M:%S"
        time = datetime.strptime(timeString, fmt)
        time = time.replace(tzinfo=pytz.timezone("EST"))
        self.time = time
    
    def get_time(self):
        return self.time
#def test3BeforeAndAfterTrigger(self):
#
#    dt = timedelta(seconds=5)
#    now = datetime(2016, 10, 12, 23, 59, 59)
#    ancient = NewsStory('', '', '', '', datetime(1987, 10, 15))
#    just_now = NewsStory('', '', '', '', now - dt)
#    in_a_bit = NewsStory('', '', '', '', now + dt)
#    future = NewsStory('', '', '', '', datetime(2087, 10, 15))
#
#    s1 = BeforeTrigger('12 Oct 2016 23:59:59')
#    s2 = AfterTrigger('12 Oct 2016 23:59:59')
#
#    self.assertTrue(s1.evaluate(ancient), "BeforeTrigger failed to fire on news from long ago")
#    self.assertTrue(s1.evaluate(just_now), "BeforeTrigger failed to fire on news happened right before specified time")
#
#    self.assertFalse(s1.evaluate(in_a_bit), "BeforeTrigger fired to fire on news happened right after specified time")
#    self.assertFalse(s1.evaluate(future), "BeforeTrigger fired to fire on news from the future")
#
#    self.assertFalse(s2.evaluate(ancient), "AfterTrigger fired to fire on news from long ago")
#    self.assertFalse(s2.evaluate(just_now), "BeforeTrigger fired to fire on news happened right before specified time")
#
#    self.assertTrue(s2.evaluate(in_a_bit), "AfterTrigger failed to fire on news just after specified time")
#    self.assertTrue(s2.evaluate(future), "AfterTrigger failed to fire on news from long ago")


def firstBeforeAndAfterTrigger_test():
    from datetime import timedelta
    dt = timedelta(seconds = 5)
    now = datetime(2016, 10, 12, 23, 59, 59)
    ancient = NewsStory('', '', '', '', datetime(1987, 10, 15))
    just_now = NewsStory('', '', '', '', now - dt)
    in_a_bit = NewsStory('', '', '', '', now + dt)
    future = NewsStory('', '', '', '', datetime(2087, 10, 15))    
    s1 = BeforeTrigger('12 Oct 2016 23:59:59')
    s2 = AfterTrigger('12 Oct 2016 23:59:59')
    assert s1.evaluate(ancient)
    assert s1.evaluate(just_now)
    assert not s1.evaluate(in_a_bit)
    assert not s1.evaluate(future)
    assert not s2.evaluate(ancient)
    assert not s2.evaluate(just_now)
    assert s2.evaluate(in_a_bit)
    assert s2.evaluate(future)


#    def test3altBeforeAndAfterTrigger(self):
#
#        dt = timedelta(seconds=5)
#        now = datetime(2016, 10, 12, 23, 59, 59)
#        now = now.replace(tzinfo=pytz.timezone("EST"))
#        
#        ancient_time = datetime(1987, 10, 15)
#        ancient_time = ancient_time.replace(tzinfo=pytz.timezone("EST"))
#        ancient = NewsStory('', '', '', '', ancient_time)
#        
#        just_now = NewsStory('', '', '', '', now - dt)
#        in_a_bit = NewsStory('', '', '', '', now + dt)
#        
#        future_time = datetime(2087, 10, 15)
#        future_time = future_time.replace(tzinfo=pytz.timezone("EST"))
#        future = NewsStory('', '', '', '', future_time)
#
#
#        s1 = BeforeTrigger('12 Oct 2016 23:59:59')
#        s2 = AfterTrigger('12 Oct 2016 23:59:59')
#
#        self.assertTrue(s1.evaluate(ancient), "BeforeTrigger failed to fire on news from long ago")
#        self.assertTrue(s1.evaluate(just_now), "BeforeTrigger failed to fire on news happened right before specified time")
#
#        self.assertFalse(s1.evaluate(in_a_bit), "BeforeTrigger fired to fire on news happened right after specified time")
#        self.assertFalse(s1.evaluate(future), "BeforeTrigger fired to fire on news from the future")
#
#        self.assertFalse(s2.evaluate(ancient), "AfterTrigger fired to fire on news from long ago")
#        self.assertFalse(s2.evaluate(just_now), "BeforeTrigger fired to fire on news happened right before specified time")
#
#        self.assertTrue(s2.evaluate(in_a_bit), "AfterTrigger failed to fire on news just after specified time")
#        self.assertTrue(s2.evaluate(future), "AfterTrigger failed to fire on news from long ago")


def secondBeforeAndAfterTrigger_test():
        dt = timedelta(seconds=5)
        now = datetime(2016, 10, 12, 23, 59, 59)
        now = now.replace(tzinfo=pytz.timezone("EST"))
        
        ancient_time = datetime(1987, 10, 15)
        ancient_time = ancient_time.replace(tzinfo=pytz.timezone("EST"))
        ancient = NewsStory('', '', '', '', ancient_time)
        
        just_now = NewsStory('', '', '', '', now - dt)
        in_a_bit = NewsStory('', '', '', '', now + dt)
        
        future_time = datetime(2087, 10, 15)
        future_time = future_time.replace(tzinfo=pytz.timezone("EST"))
        future = NewsStory('', '', '', '', future_time)

        s1 = BeforeTrigger('12 Oct 2016 23:59:59')
        s2 = AfterTrigger('12 Oct 2016 23:59:59')
        
        assert s1.evaluate(ancient)
        assert s1.evaluate(just_now)
        
        assert not s1.evaluate(in_a_bit)
        assert not s1.evaluate(future)
        
        assert not s2.evaluate(ancient)
        assert not s2.evaluate(just_now)
        
        assert s2.evaluate(in_a_bit)
        assert s2.evaluate(future)
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, timeString):
        super(BeforeTrigger, self).__init__(timeString)
    
    def evaluate(self, story):
        pub_dt = story.get_pubdate()
        if pub_dt.tzinfo == None:
            time = self.time.replace(tzinfo = None)
            return pub_dt < time
        return pub_dt < self.time

    def __str__(self):
        return "Triggered by dates before: "+str(self.time)
    
    def __repr__(self):
        return "BeforeTrigger('"+self.time.strftime("%d %b %Y %H:%M:%S")+"')"
    
    def __eq__(self, another):
        return isinstance(another, BeforeTrigger) and self.time == another.time
    
def test_BeforeTrigger():
    bt = BeforeTrigger("3 Oct 2016 17:00:10")
    print(bt)
    bt_repr = bt.__repr__()
    print(bt_repr)
    copy = eval(bt_repr)
    print(copy)
    assert bt == copy
    assert copy == bt
    
    
class AfterTrigger(TimeTrigger):
    def __init__(self, timeString):
        super(AfterTrigger, self).__init__(timeString)
    
    def evaluate(self, story):
        pub_dt = story.get_pubdate()
        if pub_dt.tzinfo == None:
            time = self.time.replace(tzinfo = None)
            return pub_dt > time
        return pub_dt > self.time
    
    def __str__(self):
        return "Triggered by dates after: "+str(self.time)
    
    def __repr__(self):
        return "AfterTrigger('"+self.time.strftime("%d %b %Y %H:%M:%S")+"')"
    
    def __eq__(self, another):
        return isinstance(another, AfterTrigger) and self.time == another.time

def test_AfterTrigger():
    at = AfterTrigger("3 Oct 2016 17:00:10")
    print(at)
    at_repr = at.__repr__()
    print(at_repr)
    copy = eval(at_repr)
    print(copy)
    assert at==copy
    assert copy==at


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

    def __repr__(self):
        return "NotTrigger("+self.trigger.__repr__()+")"
    
    def __str__(self):
        return "Not "+str(self.trigger)
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
    
    def __repr__(self):
        return "AndTrigger("+self.trigger1.__repr__()+","+self.trigger2.__repr__()+")"

    def __str__(self):
        """
        DOES NOT GIVE THE CORRECT OUTPUT
        """
        return str(self.trigger1)+" AND "+str(self.trigger2)
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)
    
    def __repr__(self):
        return "OrTrigger("+self.trigger1.__repr__()+","+self.trigger2.__repr__()+")"
    
    def __str__(self):
        """
        DOES NOT GIVE THE CORRECT OUTPUT
        """
        return str(self.trigger1)+" OR "+str(self.trigger2)
    
#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    #TODO: Problem 10
    #This is a placeholder
    #(we're just returning all the stories, with no filtering)
    filtered=[]
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered.append(story)
                break
    return filtered     
#    return stories   



def processLine(d, s):
    """
    Assumes d is a dictionary string->Trigger and that s is a string of the form
    <triggerName>,<Trigger_subclass_descriptor>,<comma_delimited_sequence_of_params_associated_w/_trigger_subclass_instance>
    params: d, a dictionary; s, a string
    
    modifies d according to the content of s
    """
    elems = s.rstrip().split(",")
    triggerName = elems[0]
    trigger_subclass_identifier = elems[1].title()
    argsToPass = elems[2:]
    singleArgSubclasses = ["Title","Description","Not","Before","After"]
    twoArgSubclasses = ["And","Or"]
    cName = trigger_subclass_identifier + "Trigger" #cName is the full Trigger subclass name
    evalExp = cName+"(*argsToPass)"
    d[triggerName] = eval(evalExp)


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    f = open(filename, 'r')
    triggerDict = {}
    triggerList = []
    for line in f:
        line = line.rstrip() #strip trailing whitespace from line
        if len(line)!=0 and (not line.startswith("//")):
            #if line doesn't start with "ADD", add content associated with line to dictionary
            #triggerDict
            if not line.startswith("ADD"):
                processLine(triggerDict, line)
            else:
                items = line.split(",")[1:]
                for k in items:
                    if k in triggerDict:
                        triggerList.append(triggerDict[k])
    return triggerList
            
            
#    trigger_file = open(filename, 'r')
#    lines = []
#    for line in trigger_file:
#        line = line.rstrip()
#        if not (len(line) == 0 or line.startswith('//')):
#            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

#    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())
        
        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)

    
def test_read_config_file():
    triggers = read_trigger_config("triggers.txt")
    for trigger in triggers:
        print(trigger)

def test_full_application():
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

if __name__ == '__main__':
    #test_read_config_file()
    test_full_application()



