import subprocess
from tqdm import tqdm
from os.path import isfile
import sys
import itertools

# TODO: more refactoring to allow for match and combo running together

# TODO: a better way to feed args to this script and its methods

# count the number of times a substring appears in a run output and flush output to a file
def outputSubstrCount(command, substrToMatch, outPath='error.log', runCount=100):
  
  # init counter of matches and flag for whether the outPath is being newly created 
  wordCount = 0
  freshFileFlag = False

  # check to set freshFileFlag
  if(isfile(outPath)):
    print(f'[INFO ]: Out file {outPath} will be overwritten.')
  else:
    print(f'[INFO ]: Out file {outPath} will be created.')
    freshFileFlag = True
  
  # overwrite or create outPath
  try:
    with open(outPath, "w") as outFileObj:
      outFileObj.write('')
  except Exception as e:
    print("[ERROR]: HUH. Exception below.")
    print(e)
    sys.exit(1)

  if freshFileFlag:
    print(f'[INFO ]: Out file {outPath} created.')
  else:
    print(f'[INFO ]: Out file {outPath} overwritten.')

  # list for capturing the matched runs 
  matchedRuns = []

  # loop with tqdm to display current progress
  for run in tqdm(range(runCount)):

    # open process with command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # get output and decode
    output, _ = process.communicate()
    outputDecoded = output.decode("utf-8")
    
    # count for substrToMatch in this run
    thisRunWordCount = outputDecoded.count(substrToMatch)

    # if any occurrences found, flush output to outPath
    if thisRunWordCount:
      tqdm.write(f'[MATCH]: Match at run {run+1}')
      tqdm.write(outputDecoded)
      matchedRuns.append(run + 1)
      with open(outPath, 'a') as outFileObj:
        outFileObj.write(outputDecoded)
        outFileObj.write("\n\n\n\n")
      tqdm.write(f'[INFO ]: Run {run+1} output flushed to out file')
    
    # increment wordCount
    wordCount = wordCount + int(thisRunWordCount)

  return wordCount, matchedRuns

# run each possible command line argument combo and flush all outputs to a file for later inspection
def comboOutputTester(baseCommand, combosComps, outPath):
  # init flag for whether the outPath is being newly created 
  freshFileFlag = False

  # check to set freshFileFlag
  if(isfile(outPath)):
    print(f'[INFO ]: Out file {outPath} will be overwritten.')
  else:
    print(f'[INFO ]: Out file {outPath} will be created.')
    freshFileFlag = True

  # overwrite or create outPath  
  try:
    with open(outPath, "w") as outFileObj:
      outFileObj.write('')
  except:
    print("[ERROR]: HUH")

  if freshFileFlag:
    print(f'[INFO ]: Out file {outPath} created.')
  else:
    print(f'[INFO ]: Out file {outPath} overwritten.')
  
  # make all combination of args
  combosMade = [combo for combo in itertools.product(*combosComps)]
  for combo in combosMade:
    print(combo)
    print(" ".join(combo))
  if type(baseCommand) is list:
    combosMade = [baseCommand[0]+" "+" ".join(combo)+" "+baseCommand[1] for combo in combosMade]
  else:
    combosMade = [baseCommand+" "+" ".join(combo) for combo in combosMade]
  
  # loop with tqdm to display current progress
  for run in tqdm(range(len(combosMade))):
    tqdm.write(f"[INFO ]: NOW RUNNING: {combosMade[run]}")

    # open process with current combo command
    process = subprocess.Popen(combosMade[run], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      
    # get output and decode
    output, _ = process.communicate()
    outputDecoded = output.decode("utf-8")

    tqdm.write(f'[INFO ]: Run complete, command: {combosMade[run]}')

    # flush output to outPath
    with open(outPath, 'a') as outFileObj:
        outFileObj.write(f"---------------\nRUN: {combosMade[run]}\n---------------")
        outFileObj.write(outputDecoded)
        outFileObj.write("\n\n\n\n")
    tqdm.write(f'[INFO ]: Run {run+1} output flushed to out file')


# to run: \/

# command = "java PA14GradientDescent softmax" 
# wordToMatch = "FATAL"
# outPath = 'error_softmax.log'
# 
# wordCount, errorRuns = outputSubstrCount(command, wordToMatch, outPath)
# 
# print(f"Number of occurrences of '{wordToMatch}': {wordCount}")
# errorRuns = ', '.join([str(i) for i in errorRuns])
# print(f'Errors at runs: {errorRuns}')


# baseCommand = ["java PA14GradientDescent", "100 0.03 0.0001 0.9 2 4 6"]
# combos = [['and', 'or', 'xor', 'iris'], ['stochastic', 'minibatch', 'batch'], ['3', '5', '7'], ['l1_norm', 'l2_norm', 'svm', 'softmax']]
# comboOutputTester(baseCommand, combos, 'runs.log')