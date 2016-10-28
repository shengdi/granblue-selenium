from selenium import webdriver
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, \
  WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import sys, time
import datetime
from twitter import get_raid_id, get_bahamut_id

profile = "C:\\Python27\\MyStuff\\selenium"
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=%s" % profile)
driver = webdriver.Chrome(chrome_options=options)

#Also have to figure out what to do about those weird popups about events
raid_count = 0
extra_count = 0
ap_slow = 0
bp_slow = 0



#def wait_until_class(classname):
#  try:
#    WebDriverWait(driver,10).until(
#      EC.presence_of_element_located((By.CLASS_NAME,classname))
#    )
#  except Exception, e:
#    print "Error"
#    sys.exit()

def wait_until_class(classname):
  WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.CLASS_NAME,classname))
  )

#Create our own click handler
#That resizes if unable to click
#That moves screen to end if unable to click
def try_click(ele):
  try:
    ele.click()
  except Exception, e:
    #Add in clicks to resize
    #Move to end of screen
    actions = ActionChains(driver)
    #actions.send_keys(Keys.END).perform()
    actions.send_keys(Keys.END).perform()
    actions.move_to_element(driver.find_elements_by_class_name("cnt-global-footer")[0]).perform()
    #ele.send_keys(Keys.END)
    #container = driver.find_elements_by_class_name("prt-lead")[0]
    #actions.move_to_element(container)
    #container.send_keys(Keys.END)
    ele.click()

def click_displayed(ele):
  print 'trying to click %s' % ele
  while True:
    auto = driver.find_elements_by_class_name(ele)[0]
    if auto.is_displayed():
      auto.click()
      print '%s clicked !' % ele
      break
    time.sleep(1)
  return
    

def do_claim_rewards():
  if wait_check("btn-usual-ok") == True:
    cancel_ok = driver.find_elements_by_class_name("btn-usual-ok")[0]
    try_click(cancel_ok)
  time.sleep(2)
  wait_until_class("lis-raid")
  r_list = driver.find_elements_by_class_name("lis-raid")
  for r in r_list:
    print 'claiming reward - did not join raid'
    r.click()
  if wait_check("btn-usual-ok") == True:
    cancel_ok = driver.find_elements_by_class_name("btn-usual-ok")[0]
    try_click(cancel_ok)

def manual_claim_rewards():
  driver.get("http://game.granbluefantasy.jp/#quest/assist/unclaimed")
  try:
    WebDriverWait(driver,10).until(
      EC.presence_of_element_located((By.CLASS_NAME,"lis-raid"))
    )
  except Exception, e:
    print 'No rewards found'
    return False
  time.sleep(2)
  r_list = driver.find_elements_by_class_name("prt-button-cover")
  for r in r_list:
    print 'claiming reward'
    r.click()
  if wait_check("btn-usual-ok") == True:
    cancel_ok = driver.find_elements_by_class_name("btn-usual-ok")[0]
    try_click(cancel_ok)
    print 'claimed reward'

def do_raid():
  driver.get("http://game.granbluefantasy.jp/#quest/assist")
  wait_until_class("lis-raid")
  bp = check_bp()
  print 'current bp: %d' % bp
  global bp_slow
  bp_slow = 0
  if bp < 2:
    print 'slowing down, not enough bp: %d' % bp
    print "checking rewards"
    manual_claim_rewards()
    bp_slow = 1
    return

  #Find Tiamat Omega
  r_list = driver.find_elements_by_class_name("lis-raid")
  found = False
  for r in r_list:
    r_name = r.get_attribute("data-chapter-name")
    if "Leviathan Omega" in r_name:
      if len(r.find_elements_by_class_name("ico-enter")) == 0:
        #If its not already joined...
        #Lets join !
        print 'joining raid: %s' % r_name
        found = True
        r.click()
  #Maybe just check twitter directly
  twitter = False
  if found != True:
    print "No Leviathan Omega Found"
    print "Getting from twitter"
    evnt = driver.find_element_by_id("tab-id")
    evnt.click()
    raidid = get_raid_id()
    print 'raid id: %s' % raidid
    while True:
      input_id = driver.find_elements_by_class_name("frm-battle-key")[0]
      if input_id.is_displayed():
        input_id.send_keys(raidid)
        print 'keys sent !'
        break
    post_key = driver.find_elements_by_class_name("btn-post-key")[0]
    post_key.click()



  #Look for twiiter ID and enter..
    #if twitter != True:
    #print "checking rewards"
    #manual_claim_rewards()
    #return
  if wait_check("btn-supporter") == False:
    do_claim_rewards()
    return
  #wait_until_class("btn-supporter")
  supporter_list = driver.find_elements_by_class_name("lis-supporter")
  support_levels = driver.find_elements_by_class_name("txt-summon-level")
  highest_lvl = 0
  for supports in supporter_list:
    levels = supports.find_elements_by_class_name("txt-summon-level")[0] 
    if levels.text == "":
      continue
    lvl = int(levels.text.split()[1])
    print lvl
    selected_support = supports
    break
  try_click(selected_support.find_elements_by_class_name("prt-button-cover")[0])

  #Now OK for party..no need to think too much
  wait_until_class("se-quest-start")
  try_click(driver.find_elements_by_class_name("se-quest-start")[0])
  attack_and_quit()
  print "Finished one session"
  return

def bahamut_force():
  while True:
    do_bahamut_raid()
    time.sleep(2)

def do_bahamut_raid():
  #driver.get("http://game.granbluefantasy.jp/#quest/assist")




  print "Getting from twitter"
  #evnt = driver.find_element_by_id("tab-id")
  #evnt.click()
  raidid = get_bahamut_id()
  print 'raid id: %s' % raidid
  while True:
    input_id = driver.find_elements_by_class_name("frm-battle-key")[0]
    if input_id.is_displayed():
      input_id.clear()
      input_id.send_keys(raidid)
      print 'keys sent !'
      break
  post_key = driver.find_elements_by_class_name("btn-post-key")[0]
  post_key.click()



  #Look for twiiter ID and enter..
    #if twitter != True:
    #print "checking rewards"
    #manual_claim_rewards()
    #return
  if wait_check("btn-supporter") == False:
    #do_claim_rewards()
    print 'Already full, try again'
    driver.find_elements_by_class_name("btn-usual-ok")[0].click()
    return
  #wait_until_class("btn-supporter")
  supporter_list = driver.find_elements_by_class_name("lis-supporter")
  support_levels = driver.find_elements_by_class_name("txt-summon-level")
  highest_lvl = 0
  for supports in supporter_list:
    levels = supports.find_elements_by_class_name("txt-summon-level")[0] 
    if levels.text == "":
      continue
    lvl = int(levels.text.split()[1])
    print lvl
    selected_support = supports
    break
  try_click(selected_support.find_elements_by_class_name("prt-button-cover")[0])

  #Now OK for party..no need to think too much
  wait_until_class("se-quest-start")
  try_click(driver.find_elements_by_class_name("se-quest-start")[0])
  attack_and_quit()
  print "Finished one session"
  return

def check_bp():
  wait_until_class("prt-user-bp-value")
  bp = driver.find_elements_by_class_name("prt-user-bp-value")[0]
  num = bp.get_attribute("title")
  return (int)(num)
  
def check_ap():
  wait_until_class("txt-stamina-value")
  bp = driver.find_elements_by_class_name("txt-stamina-value")[0]
  total = bp.get_attribute("title")
  num = total.split("/")[0]
  print num
  return (int)(num)
  
  
def do_free_quest():
  #manually start site and go to quest list
  #check ap also..
  
  #prt-quest-thumb img-quest src has to be this
  #thumb = "http://game-a1.granbluefantasy.jp/assets_en/img_mid/sp/quest/assets/free/20003_02.jpg"
  thumb = "http://game-a1.granbluefantasy.jp/assets_en/img_mid/sp/quest/assets/free/20003_01.jpg"

  #reward has to be ico-stone

  #First find the quests...
  q_list = driver.find_elements_by_class_name("prt-list-contents")
  for l in q_list:
    questname = l.find_elements_by_class_name("txt-quest-title")
    select = l.find_elements_by_class_name("prt-button-cover")
    print questname[0].text
    #Check if conditions are true
    thumbnail = l.find_elements_by_class_name("img-quest")[0].get_attribute("src")
    is_stone = l.find_elements_by_class_name("ico-stone")
    if thumbnail == thumb and is_stone != []:
      select[0].click()
  select_party()
  wait_until_class("btn-skip")
  skip = driver.find_elements_by_class_name("btn-skip")[0]
  skip.click()
  attack_then_auto()
  end_quest()
  return


def select_party():
  #select supports
  wait_until_class("btn-supporter")
  supporter_list = driver.find_elements_by_class_name("lis-supporter")
  support_levels = driver.find_elements_by_class_name("txt-summon-level")
  highest_lvl = 0
  for supports in supporter_list:
    levels = supports.find_elements_by_class_name("txt-summon-level")[0] 
    if levels.text == "":
      continue
    lvl = int(levels.text.split()[1])
    print lvl
    #Test last
    selected_support = supports
    break
    #if lvl > highest_lvl:
    #  highest_lvl = lvl
    #  selected_support = supports
    #  print highest_lvl
  try_click(selected_support.find_elements_by_class_name("prt-button-cover")[0])

  #Now OK for party..no need to think too much
  wait_until_class("se-quest-start")
  try_click(driver.find_elements_by_class_name("se-quest-start")[0])
  time.sleep(5)


def do_extra_quest(questname, difficulty):
  driver.get("http://game.granbluefantasy.jp/#quest/extra")

  #WTF OK THE RESIZING OF THE PAGE BY THE GAME MAKES THINGS GO HAYWIRE
  #JUST REMEMBER TO SWITCH TO SMALLEST SCREEN SIZE
  #wait_until_class("txt-quest-title")
  if wait_check("txt-quest-title") == False:
    do_claim_rewards()
    return
  ap = check_ap()
  global ap_slow
  ap_slow = 0 
  if ap < 15:
    print 'not enough ap: %d' % ap
    ap_slow = 1
    return



  q_list = driver.find_elements_by_class_name("prt-list-contents")
  for l in q_list:
    quest = l.find_elements_by_class_name("txt-quest-title")
    select = l.find_elements_by_class_name("btn-stage-detail")
    print quest[0].text
    #if quest[0].text == "Shiny Slime Search!":
    #if quest[0].text == "Angel Halo":
    if quest[0].text == questname:
      select[0].click()
  wait_until_class("btn-set-quest")
  #We always just go for the first one...since its the easiest..
  play_button = driver.find_elements_by_class_name("btn-set-quest")
  for p in play_button:
    #if p.get_attribute("data-chapter-name") == "Shiny Slime Search!":
    if p.get_attribute("data-chapter-name") == questname:
      if p.get_attribute("data-difficulty") == difficulty:
        p.click()
  #Now we need to choose supports..
  #We just get the highest level...

  #Bah just pick the first one...we can't seem to scroll down without first
  #manually clicking on the browser...
  wait_until_class("btn-supporter")
  supporter_list = driver.find_elements_by_class_name("lis-supporter")
  support_levels = driver.find_elements_by_class_name("txt-summon-level")
  highest_lvl = 0
  for supports in supporter_list:
    levels = supports.find_elements_by_class_name("txt-summon-level")[0] 
    if levels.text == "":
      continue
    lvl = int(levels.text.split()[1])
    print lvl
    #Test last
    selected_support = supports
    break
    #if lvl > highest_lvl:
    #  highest_lvl = lvl
    #  selected_support = supports
    #  print highest_lvl
  try_click(selected_support.find_elements_by_class_name("prt-button-cover")[0])

  #Now OK for party..no need to think too much
  wait_until_class("se-quest-start")
  try_click(driver.find_elements_by_class_name("se-quest-start")[0])
  time.sleep(5)
  #attack_till_end_of_quest()
  attack_then_auto()
  end_quest_no_scene()
  print 'One quest done !'

def wait_pass(classname):
  #If button does not appear, click something else
  try:
    WebDriverWait(driver,2).until(
      EC.presence_of_element_located((By.CLASS_NAME,classname))
    )
  except Exception, e:
    pass

def wait_check(classname):
  #Break out of name if class appears
  try:
    WebDriverWait(driver,10).until(
      EC.presence_of_element_located((By.CLASS_NAME,classname))
    )
    return True
  except Exception, e:
    return False

def try_click_pass(ele):
  try:
    ele.click()
  except Exception, e:
    pass

#Just click attack/next until it does not appear
def attack_till_end_of_quest():
  while(True):
    #Just try freaking clicking all these things until they work...
    #if wait_check("btn-attack-start") == True:
    atk = driver.find_elements_by_class_name("btn-attack-start")[0]
    if atk.get_attribute("class") == u'btn-attack-start display-on':
      try_click_pass(atk)
    #if wait_check("btn-result") == True:
    nxt = driver.find_elements_by_class_name("btn-result")[0]
    try_click_pass(nxt)
    #Stop when this appears
    adv = driver.find_elements_by_class_name("prt-advice")[0]
    try_click_pass(adv)
    if wait_check("txt-rankpt") == True:
      break
  end = driver.find_elements_by_class_name("btn-usual-ok")[0]
  try_click(end)
  global extra_count
  extra_count += 1
  wait_until_class("btn-control")
  #Just go back to quest through URL
  #back_to_quest = driver.find_elements_by_class_name("btn-control")[0]
  #try_click(back_to_quest)
  #wait_until_class("btn-usual-cancel")
  #cancel_friend = driver.find_elements_by_class_name("btn-usual-cancel")[0]
  #try_click(cancel_friend)


#Alright this should be easier
def attack_and_quit():
  #Cancel request
  time.sleep(5)
  if wait_check("btn-usual-cancel") == True:
    time.sleep(5)
    print 'Cancelling request'
    cancel_friend = driver.find_elements_by_class_name("btn-usual-cancel")[0]
    try:
      cancel_friend.click()
    except Exception, e:
      print 'cannot cancel, trying to click ok'
      cancel_ok = driver.find_elements_by_class_name("btn-usual-ok")[0]
      try_click(cancel_ok)

  #wait_until_class("btn-usual-cancel")


  print 'Attacking'
  time.sleep(2)
  wait_until_class("btn-attack-start")
  while(True):
    atk = driver.find_elements_by_class_name("btn-attack-start")[0]
    if atk.get_attribute("class") == u'btn-attack-start display-on':
      try:
        print 'trying to attack !'
        atk.click()
        global raid_count
        raid_count += 1
        print 'returning from attack_and_quit, slowing down..'
        #time.sleep(300)
        time.sleep(60)
        break
      except Exception, e:
        pass
    else:
      print 'Already dead ? returning'
      break

def attack_then_auto():
  print 'First Attack'
  wait_until_class("btn-attack-start")
  click_displayed("btn-attack-start")
  wait_until_class("btn-auto")
  while True:
    auto = driver.find_elements_by_class_name("btn-auto")[0]
    if auto.is_displayed():
      auto.click()
      break
  global extra_count
  extra_count += 1
  return

def end_quest_no_scene():
  while True:
    time.sleep(5)
    if "result" in driver.current_url:
      break
  wait_until_class("btn-usual-ok")
  click_displayed("btn-usual-ok")

def check_is_cocytus():
  is_cocytus = False
  monsters = driver.find_elements_by_class_name('btn-targeting')
  for i in monsters:
    monster_name = i.find_elements_by_class_name('name')[0].get_attribute('innerHTML')
    if "Cocytus" in monster_name:
      is_cocytus = True

  return is_cocytus

def check_skills():
  #returns array of skill data
  characters = driver.find_elements_by_class_name('btn-command-character')
  #Get first 4 only...
  print 'getting skill data'
  c = []
  for i in range(4):
    ability = []
    character = characters[i]
    abilities = character.find_elements_by_class_name('lis-ability-state')
    for a in abilities:
      ability.append(a.get_attribute('state'))
    c.append(ability)
  return c

def cast_skill(c, s):
  #Click character
  print 'casting skill %d from char %d' % (s, c)
  click_displayed("lis-character%d" % c)

  #Click skill
  chara_num = driver.find_elements_by_class_name("chara%d" % (c+1))[0]
  chara_abt = chara_num.find_elements_by_class_name("lis-ability")[s]
  while True:
    if chara_abt.is_displayed():
      chara_abt.click()
      print 'skill clicked !'
      break
    time.sleep(1)
  #Click back
  click_displayed("btn-command-back")
  return

def check_ca_gauge():
  print 'getting ca gauges'
  characters = driver.find_elements_by_class_name('prt-gauge-special-inner')
  c = []
  for i in range(4):
    percent = characters[i].get_attribute('style').split()[1]
    c.append(int(percent[0:-2]))
  return c

def check_ca_lock():
  print 'getting ca cast status'
  lock = driver.find_elements_by_class_name('btn-lock')[0]
  status = lock.get_attribute('class').split()[1]
  if status == u'lock0':
    print 'ca is on'
    return True
  elif status == u'lock1':
    print 'ca is off'
    return False

def switch_ca(s):
  lock = driver.find_elements_by_class_name('btn-lock')[0]
  status = lock.get_attribute('class').split()[1]
  if status == u'lock0' and s == False:
    #Switch off ca
    lock.click()
  elif status == u'lock1' and s == True:
    #Switch on ca
    lock.click()
  return
    
def check_health():
  print 'getting health'
  characters = driver.find_elements_by_class_name('prt-gauge-hp-inner')
  c = []
  for i in range(4):
    percent = characters[i].get_attribute('style').split()[1]
    c.append(int(percent[0:-2]))
  return c

def check_summons():
  print 'getting summon availability'
  summons = driver.find_elements_by_class_name('lis-summon')
  c = []
  for s in summons:
    classes = s.get_attribute("class").split()
    for what in classes:
      if what == u'off':
        c.append(what)
      if what == u'on':
        c.append(what)
  return c

def get_turn():
  print 'trying to get turn number'
  n = driver.find_elements_by_class_name('prt-number')[0]
  turn = n.find_element_by_tag_name('div').get_attribute('class')
  if turn != u'':
    num = int(turn[-1])
    return num
  else:
    return 0

def cast_summon(c):
  print 'casting summon %d' % c
  #Click summon button
  click_displayed('btn-command-summon')
  time.sleep(1)
  #btn-summon-use ?

  #Click summon number c
  summons = driver.find_elements_by_class_name('lis-summon')
  selected_summon = summons[c]
  while True:
    if selected_summon.is_displayed():
      selected_summon.click()
      print 'summon clicked !'

      click_displayed('btn-summon-use')
      print 'summon confirmed'
      break
    time.sleep(1)

def cast_available_summons():
  summons = check_summons()
  print summons
  for i,j in enumerate(summons):
    if j == u'on':
      print 'casting summon %d' % i
      cast_summon(i)
      time.sleep(7)
      break

  return

def cast_buffs():
  skills = check_skills()

  buff_config = [[0,1],[0,2],[0,3],[1,0],[1,2],[3,0]]

  for buff in buff_config:
    if skills[buff[0]][buff[1]] == u'2':
      cast_skill(buff[0],buff[1])
      time.sleep(4)
  return

def boss_loop():
  try:
    while True:
      try:
        fight_cocytus()
        time.sleep(5)
      except WebDriverException, e:
        print e
        print 'blah cannot click etc ignore'
  except Exception, e:
    print e
    print 'oh no'

def fight_cocytus():
  #Check state

  #First check if targeting area is there
  battle = driver.find_elements_by_class_name("prt-targeting-area")[0]
  if battle.is_displayed() != True:
    return

  nxt = driver.find_elements_by_class_name("btn-result")[0]
  if nxt.is_displayed():
    nxt.click()
    return
  #Check monster  
  #if check_is_cocytus() == True:
  if True:
    #Fight cocytus
    skills = check_skills()
    cast_buffs()
    cast_available_summons()

    #Heal
    health = check_health()
    if skills[2][0] == u'2':
      for h in health:
        if h < 40:
          cast_skill(2,0)
          time.sleep(3)
          break

    #Delay
    turn = get_turn()
    if turn > 1:
      if skills[0][0] == u'2':
        cast_skill(0,0)
        time.sleep(4)
      if skills[3][1] == u'2':
        cast_skill(3,1)
        time.sleep(4)

    #check ca
    ca = check_ca_gauge()
    ca_count = 0
    ca_attack = False
    for cag in ca:
      if cag == 100:
        ca_count += 1
    if ca_count == 4:
      switch_ca(True)
      #ca attack takes forever
      ca_attack = True
    else:
      switch_ca(False)

    #attack
    try_count = 0
    while True:
      adv = driver.find_elements_by_class_name("prt-advice")[0]
      atk = driver.find_elements_by_class_name("btn-attack-start")[0]
      if adv.is_displayed():
        print 'click advice'
        adv.click()
      if atk.is_displayed():
        print 'click attack'
        atk.click()
        if ca_attack == True:
          time.sleep(30)
        else:
          time.sleep(5)
        break
      print 'no attack or advice'
      try_count += 1
      if try_count > 10:
        break
      time.sleep(2)

    #Move these into a checkbuffs function
    # if skills[0][1] == u'2':
    #   cast_skill(0,1) #Cast mist
    # elif skills[0][2] == u'2':
    #   cast_skill(0,2) #Cast delay
    # elif skills[0][3] == u'2':
    #   cast_skill(0,3) #Cast rage
    # elif skills[1][0] == u'2':
    #   cast_skill(1, 0) #Butterfly
    # elif skills[1][2] == u'2':
    #   cast_skill(1, 2) #Crit
    # elif skills[3][0] == u'2':
    #   cast_skill(3,0) #Forewarning



  else:
    skills = check_skills()
    #if naru's buff is available, cast
    #otherwise, just attack
    if skills[1][0] == u'2':
      cast_skill(1, 0) #Butterfly
    elif skills[1][2] == u'2':
      cast_skill(1, 2) #Crit
    else:
      #attack
      try_count = 0
      while True:
        adv = driver.find_elements_by_class_name("prt-advice")[0]
        atk = driver.find_elements_by_class_name("btn-attack-start")[0]
        if adv.is_displayed():
          print 'click advice'
          adv.click()
        if atk.is_displayed():
          print 'click attack'
          atk.click()
          time.sleep(5)
          break
        print 'no attack or advice'
        try_count += 1
        if try_count > 10:
          break
        time.sleep(2)




  #Buff naru

  #Clear creeps

  #Buff then cast summon

  #Keep attacking and buffing

  #
  

def end_quest():

  #Check title change..
  while True:
    if "result" in driver.current_url:
      break
  wait_until_class("btn-usual-ok")
  click_displayed("btn-usual-ok")
  wait_until_class("btn-control")
  click_displayed("btn-control")
  wait_until_class("btn-usual-ok")
  click_displayed("btn-usual-ok")
  wait_until_class("btn-skip")
  click_displayed("btn-skip")

def trial_loop():
  while True:
    try:
      #do_extra_quest("Scarlet Trial", "1")
      do_extra_quest("Cerulean Trial", "2")
    except Exception, e:
      print "Error Trial: %s" % e
    time.sleep(500)
    print 'succesful trials: %s' % extra_count



def raid_loop():
  while True:
    try:
      do_raid()
    except UnexpectedAlertPresentException, e:
      #Try to click alerts..
      print 'Alert popup'
      driver.switch_to_alert().accept()
    except Exception, e:
      print "Error Raid: %s" % e
    if bp_slow == 1:
      #print 'Wait 30 mins'
      #time.sleep(1800)
      print 'Wait 20 mins'
      time.sleep(1200)
    else:
      print 'Wait 30s'
      time.sleep(30)
    print '%s succesful raids: %s' % (datetime.datetime.now().__str__(), raid_count)

def extra_loop():
  while True:
    try:
      do_extra_quest("Scarlet Trial", "2")
    except UnexpectedAlertPresentException, e:
      #Try to click alerts..
      print 'Alert popup'
      driver.switch_to_alert().accept()
    except Exception, e:
      print "Error Quest: %s" % e
    if ap_slow == 1:
      print 'Wait 5 mins'
      time.sleep(300)
    else:
      print 'Wait 30s'
      time.sleep(30)
    print '%s succesful quests: %s' % (datetime.datetime.now().__str__(), extra_count)

def raid_and_extra_loop():
  global ap_slow
  global bp_slow
  while True:
    if bp_slow == 0:
      try:
        do_raid()
      except UnexpectedAlertPresentException, e:
        #Try to click alerts..
        print 'Alert popup'
        driver.switch_to_alert().accept()
      except Exception, e:
        print "Error Raid: %s" % e
    if ap_slow == 0:
      try:
        do_extra_quest("Violet Trial", "2")
      except UnexpectedAlertPresentException, e:
        #Try to click alerts..
        print 'Alert popup'
        driver.switch_to_alert().accept()
      except Exception, e:
        print "Error Quest: %s" % e
    if ap_slow == 1 and bp_slow == 1:
      print 'Wait 1 hour'
      time.sleep(3600)
      ap_slow = 0
      bp_slow = 0
    else:
      print 'Wait 30s'
      time.sleep(30)
    print '%s succesful quests: %s' % (datetime.datetime.now().__str__(), extra_count)
    print '%s succesful raids: %s' % (datetime.datetime.now().__str__(), raid_count)

def play_poker():
  #10chip
  #driver.get("http://game.granbluefantasy.jp/#casino/game/poker/200020")

  #100chip - time to go bust
  #driver.get("http://game.granbluefantasy.jp/#casino/game/poker/200030")

  #1000chip - sitting in the big boy table now
  driver.get("http://game.granbluefantasy.jp/#casino/game/poker/200040")

  #Alright, so from javascript get exportRoot
  #exportRoot.cards_1[0] is the type
  #exportRoot.cards_1[1] is the value

  #Deal
  wait_until_class("prt-start-shine")
  click_displayed("prt-start-shine")

  time.sleep(2)
  cards = []
  types = []
  clicks = []
  counts = {u'0':0, u'1':0, u'2':0, u'3':0, u'4':0, u'5':0}
  for i in range(1,6):
    num = driver.execute_script("return exportRoot.cards_%d[1]" % i)
    if num in cards:
      print 'cards: ' 
      print cards
      print 'num'
      print num
      #Click this..
      clicks.append(i) #Click card number i
      #Find the duplicate and append to clicks
      clicks.append(cards.index(num)+1)
    if num == u'99': 
      clicks.append(i) #Click card number i

    #Count types..
    suit = driver.execute_script("return exportRoot.cards_%d[0]" % i)
    if suit == u'99':
      #bah just ignore..since joker has been selected it won try all types..
      suit = u'0'
    counts[suit] += 1
    types.append(suit)
    cards.append(num)


  #If no duplicates found just click all of the same type..
  if len(clicks) == 0:
    for i in counts:
      if counts[i] == 4:
        #Hold all of this type..
        for j,k in enumerate(types):
          if types == i:
            clicks.append(j+1)

    
  hold = set(clicks)
  print hold

  #try x 10 y 400
  #try x 100 y 224
  
  #actions = ActionChains(driver)
  #actions.send_keys(Keys.END).perform()
  #actions.move_to_element(driver.find_elements_by_id("cav")[0]).perform()

  #0,0 is card 3
  #alright we just loop and print ba
  #for x in range(0,320,10):
  #  for y in range(0,400,10):
  #    actions = ActionsChains(client.driver)

  canv = driver.find_element_by_id("canv")
  for i in hold:
    if i == 1:
      print 'holding card 1'
      actions = ActionChains(driver)
      actions.move_to_element_with_offset(canv,20,210).click().perform()
    if i == 2:
      print 'holding card 2'
      actions = ActionChains(driver)
      actions.move_to_element_with_offset(canv,80,210).click().perform()
    if i == 3:
      print 'holding card 3'
      actions = ActionChains(driver)
      actions.move_to_element_with_offset(canv,140,210).click().perform()
    if i == 4:
      print 'holding card 4'
      actions = ActionChains(driver)
      actions.move_to_element_with_offset(canv,200,210).click().perform()
    if i == 5:
      print 'holding card 5'
      actions = ActionChains(driver)
      actions.move_to_element_with_offset(canv,260,210).click().perform()

  #Keep
  time.sleep(1)
  wait_until_class("prt-ok-shine")
  click_displayed("prt-ok-shine")


  #Check if we get to doubleup...
  #Check if prt-yes-shine and prt-no-shine is visiable...
  doubleup = False
  try:
    print 'waiting for doubleup'
    time.sleep(5)
    wait_until_class("prt-yes-shine")
    #check prt-yes, if it has display: none that means we have no doubleup
    #or check if it has display: block
    yes = driver.find_elements_by_class_name("prt-yes")[0]
    if yes.value_of_css_property('display') == u'block':
      yesc = driver.find_elements_by_class_name("prt-yes-shine")[0]
      yesc.click()
      doubleup = True
      print 'doubleup !'
    else:
      print 'no doubleup'
      return
  except Exception, e:
    print e
    print 'no doubleup'
    return

  if doubleup == True:
    count_doubleup = 0
    while count_doubleup < 11:
      time.sleep(2)
      doubleup_card_1 =  driver.execute_script("return exportRoot.doubleup_card_1[1]")
      high = driver.find_elements_by_class_name("prt-high-shine")[0]
      low = driver.find_elements_by_class_name("prt-low-shine")[0]
      high_array = [u'2',u'3',u'4',u'5',u'6',u'7']
      low_array = [u'8',u'9',u'10',u'11',u'12',u'13',u'1']

      if doubleup_card_1 in high_array:
        print 'card is %s, choosing high !' % doubleup_card_1
        click_displayed("prt-high-shine")
      elif doubleup_card_1 in low_array:
        print 'card is %s, choosing low !' % doubleup_card_1
        click_displayed("prt-low-shine")
      
      doubleup_card_2 =  driver.execute_script("return exportRoot.doubleup_card_1[1]")
      #check if fail...
      time.sleep(3)
      #check prt-yes, if it has display: none that means we have no doubleup
      check_fail = driver.find_elements_by_class_name("prt-yes")[0]
      if check_fail.value_of_css_property('display') == u'block':
        print 'doubleup succeed !'
      else:
        print 'doubleup failed..'
        return

      #if doubleup_card_2 == u'8':
      #  click_displayed("prt-no-shine")
      #  print 'met 8..not double upping..'
      #  return
      #else:
      click_displayed("prt-yes-shine")
      print 'doubleup again !'
      count_doubleup += 1
      
    #Click then check card 2, if 7 we stop..


def loop_poker():
  #Choose bet amount
  #10chip
  #driver.get("http://game.granbluefantasy.jp/#casino/game/poker/200020")
  #100chip
  #driver.get("http://game.granbluefantasy.jp/#casino/game/poker/200030")

  lost = 0
  while True:
    play_poker()
    lost += 1
    print 'Lost me %d gold' % (lost*1000)

if __name__ == "__main__":
  raid_loop()
  #extra_loop()
  #raid_and_extra_loop()

    #TODO:
    #Add summons, add ability to do events, add ability to go through simple
    #quest lists and fate episodes

    #Add state machines to handle all the different states the game is in..
    #https://github.com/tyarkoni/transitions

  #do_extra_quest("Scarlet Trial", "1")


#try:
#  WebDriverWait(driver,10).until(EC.title_contains("cheese!"))
#  print driver.title
#
#finally:
#  driver.quit()


#Attack button is class="btn-attack-start" combined with class display-on when
#when it is shown, and display-off when not shown, so wait until shown

#Also not sure if class="prt-advice" will mess up the clicking of attack button

#Also search for class="lis-summon btn_summon-available on" summon-id="supporter"
