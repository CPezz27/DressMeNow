# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestAggiungiprodotto():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_aggiungiprodotto(self):
    self.driver.get("http://127.0.0.1:5000/direttore/login")
    self.driver.set_window_size(976, 1040)
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("alrossi2@gmail.com")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("Password1234!")
    self.driver.find_element(By.CSS_SELECTOR, ".bg-green-500").click()
    self.driver.find_element(By.LINK_TEXT, "Aggiungi Prodotto").click()
    self.driver.find_element(By.ID, "nome").click()
    self.driver.find_element(By.ID, "nome").send_keys("Prodotto test 1")
    self.driver.find_element(By.ID, "marca").click()
    self.driver.find_element(By.ID, "marca").send_keys("Marca 1")
    self.driver.find_element(By.ID, "descrizione").click()
    self.driver.find_element(By.ID, "descrizione").send_keys("Descrizione 1")
    self.driver.find_element(By.ID, "prezzo").click()
    self.driver.find_element(By.ID, "prezzo").send_keys("15")
    self.driver.find_element(By.ID, "colore").click()
    self.driver.find_element(By.ID, "colore").send_keys("blu")
    self.driver.find_element(By.ID, "materiale").click()
    self.driver.find_element(By.ID, "materiale").send_keys("pelle")
    self.driver.find_element(By.CSS_SELECTOR, ".bg-blue-500").click()
    elements = self.driver.find_elements(By.CSS_SELECTOR, ".flex:nth-child(3) > .text-sm")
    assert len(elements) > 0
  