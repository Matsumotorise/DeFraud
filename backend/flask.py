from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

# Things needed:
# Search functionality

@app.route('/')
def hello_world():
   return 'Hello World'

# Retrieves json of {dateTime:dt, transactionIDs:[...], SusBools: [T,F,F, ...]}
@app.route('/blockLookup')
def blockLookup(blockNumber):


# Returns list of transaction features that michael parsed
@app.route('/transactionDetails')
def transactionDetails():



if __name__ == '__main__':
   app.run()
