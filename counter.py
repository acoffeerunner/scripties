import subprocess
from tqdm import tqdm

command = "java PA13Tests l1_norm" 
wordCount = 0

with open("error.log", "w") as outFileObj:
  outFileObj.write('')

matchedRuns = []
for run in tqdm(range(100)):
  process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  output, _ = process.communicate()

  outputDecoded = output.decode("utf-8")
  
  thisRunWordCount = outputDecoded.count("FATAL")
  if thisRunWordCount:
    tqdm.write(f'[MATCH]: Match at run {run+1}')
    tqdm.write(outputDecoded)
    matchedRuns.append(run + 1)
    with open("error.log", 'a') as outFileObj:
      outFileObj.write(outputDecoded)
      outFileObj.write("\n\n\n\n")
    tqdm.write(f'[INFO ]: Run {run+1} output flushed to out file')
  wordCount = wordCount + int(thisRunWordCount/2)

print(f"Number of occurrences of FATAL: {wordCount}")
print(f"Number of matched runs: {len(matchedRuns)}")
errorRuns = ', '.join([str(i) for i in matchedRuns])
print(f'Errors at runs: {errorRuns}')




