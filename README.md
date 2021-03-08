# frankenbot2000
An accursed bot that tweets newly minted hicetnunc.xyz NFTs and quotes from Mary Shelley's Frankenstein in the voice of Herman Munster.  Loathed by its creator  @GroffFizix

### Overview

Deployeded on AWS Lambda using a EventBridge (CloudWatch Events) trigger with the schedule expression <code>rate(7 hours)</code>. The API keys are stored in <code>KEYS.py</code>. The project is built using a virtual environment with all pip packages installed in an <code>env</code> directory. When ready for deployment, <code>lambda_function.py</code>, <code>frankenbot.txt</code>, and <code>KEYS.py</code> are copied to this directory, which is then compressed into a <code>*.zip</code> archive for upload to Lambda.
