import aiml
import os
os.chdir('/home/wangxin/alice')
alice = aiml.Kernel()
alice.learn("startup.xml")
alice.respond('LOAD ALICE')
alice.respond('hello')