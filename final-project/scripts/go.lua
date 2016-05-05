require 'nn'
require 'rnn'
require 'prepare'

opt = {
  vocabSize = 30000, -- Number of words in our vocabulary

  batchSize = 32, -- Number of sequences to train on in parallel
  seqLen = 5, -- Sequence length: BPTT for this many time-steps
  hiddenSize = 200, -- Number of hidden units used as output of each recurrent layer

  trainFrac = 0.95, -- Fraction of data that goes into training set
  valFrac = 0.05, -- Fraction of data that goes into validation set
}

-- Data
--ds = dp.PennTreeBank{recurrent=true, context_size=5}
--trainSet = ds:trainSet()
en, ja, ref = collectdata()
print(#en * opt.trainFrac)
print(ref)
