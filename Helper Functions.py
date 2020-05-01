import pickle as pk
import numpy as np
import pandas as pd


def extract_context(df, keyword, column = "words", context_len = 5):
    """
    :param df: data frame
    :param keyword: keyword for context
    :param column: which column of data contains tokens (name)
    :param len: length of context
    :return: data frame of just context words with old ID's
    """

    temp_df = df.loc[df[column] == keyword]
    leng = len(temp_df)
    print("Keyword found {} times".format(leng))

    # Get the index column as a column
    temp_df = temp_df.reset_index().set_index('index', drop=False)
    indices = temp_df['index']

    # Get the slices in tuples, in a list to iterate over
    slices = []
    for index in indices:
        slice = (max(index - context_len, 0),  min(index + context_len, len(df)))
        slices.append(slice)

    # Create a copy of the original data frame
    results = pd.DataFrame().reindex_like(df)

    # Take out just the rows with context
    for slice in slices:
        results = pd.concat([results, df.iloc[slice[0]:slice[1] + 1]])

    # Get rid of the empty rows at the start
    results = results.iloc[len(df):, ]
    return results


def ngrammer(data, indexedvocab, rtrain=.5, rtest=.3, depth=3):
    '''This function takes a text corpus (in list form), an indexed vocabulary
    (2-tuple of dictionaries: word2idx, idx2word), proportions to use for
    training, validation, and testing datasets, and desired depth of ngramms.
    It returns a dictionary of n-grams of depth n-1, with test/val/train sets. 
    Namely, it returns a list of possible n-grams "%gram", and 
    a list of associated targets "%target."
    Recall that n-gram of depth 3 is 4-gram, and so on.'''
    
    output = {}
    word_ref = indexedvocab[0] #word2id

    temp = []
    target = []
    gram = []
    j = 0; k = 0; badd = 0;
  
    for i in range(len(data)):
        if len(data[i]) <= depth:
            print("Specified depth is larger than, ",i+1,"th ", "phrase","\n")
            badd += 1
        else:
            #print(data[i])
            temp=[]
            j = 0
            k = 0
            while j < len(data[i]):
                #the wind cries mary poppins:
                #1st: the wind cries - mary
                #2nd: wind cries mary - poppins
                if ((j+1) % (depth+k+1)) > 0:
                    temp.append(word_ref[data[i][j]])
                    #print("temp:",temp)
                    j += 1
                else:
                    target.append(word_ref[data[i][j]])
                    gram.append(temp)
                    temp=[]
                    #print("target:", target)
                    j -= (depth-1)
                    k += 1
  
    print(badd,"headlines/phrases have depth >= length")
    
    #First split the training sets
    train_gram, temp_test_gram, train_target, temp_test_target = train_test_split(gram, target, train_size=rtrain, test_size=(1-rtrain), shuffle=False)
    #Create validation and testing sets
    val_gram, test_gram, val_target, test_target = train_test_split(temp_test_gram, temp_test_target, test_size=(2*rtest), train_size=(1-(2*rtest)), shuffle=False)
  
    output["train_target"] = np.array(train_target, dtype="int32")
    output["train_gram"] = np.array(train_gram, dtype="int32")
    output["val_target"] = np.array(val_target, dtype="int32")
    output["val_gram"] = np.array(val_gram, dtype="int32")
    output["test_target"] = np.array(test_target, dtype="int32")
    output["test_gram"] = np.array(test_gram, dtype="int32")
    output["vocab"] = indexedvocab
  
    return output


def get_batches(inputs, targets, batch_size, shuffle=True):
    """Divide a dataset into mini-batches of a given size. This is a 'generator', which  
    one can use in a for loop.
    inputs - input n-gramm array
    targets - target array
    batch_size - inputs % batch_size == 0
    shuffle - flag indicating whether or not to shuffle data
    """
    
    if inputs.shape[0] % batch_size != 0:
        raise RuntimeError('The number of data points must be a multiple of the batch size.')
    num_batches = inputs.shape[0] // batch_size

    if shuffle:
        idxs = np.random.permutation(inputs.shape[0])
        inputs = inputs[idxs, :]
        targets = targets[idxs]

    for m in range(num_batches):
        yield inputs[m*batch_size:(m+1)*batch_size, :], \
              targets[m*batch_size:(m+1)*batch_size]


if __name__ == "__main__":

    df = pd.DataFrame({
        "words": ["a", "b", "c", "d", "e", "f", "g", "b", "c", "d", "a"],
        "Other": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    })

    trial_1 = extract_context(df, "a", "words", context_len=2)
    print(trial_1)
    trial_2 = extract_context(df, "b", "words", context_len=2)
    print(trial_2)
