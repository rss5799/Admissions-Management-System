import numpy as np
from collections import Counter


#decision tree regression model
class Node():
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, var_red=None, value=None):
        # for decision node
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.var_red = var_red        
        # for leaf node
        self.value = value

class DecisionTreeRegressor():
    def __init__(self, min_samples_split=2, max_depth=2):
        self.root = None        
        # stopping conditions
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        
    def build_tree(self, dataset, curr_depth=0):
        X, Y = dataset[:,:-1], dataset[:,-1]
        num_samples, num_features = np.shape(X)
        best_split = {}
        # split until stopping conditions are met
        if num_samples>=self.min_samples_split and curr_depth<=self.max_depth:
            # find the best split
            best_split = self.get_best_split(dataset, num_samples, num_features)
            # check if information gain is positive
            if best_split["var_red"]>0:
                # recur left
                left_subtree = self.build_tree(best_split["dataset_left"], curr_depth+1)
                # recur right
                right_subtree = self.build_tree(best_split["dataset_right"], curr_depth+1)
                # return decision node
                return Node(best_split["feature_index"], best_split["threshold"], 
                            left_subtree, right_subtree, best_split["var_red"])
        
        # compute leaf node
        leaf_value = self.calculate_leaf_value(Y)
        # return leaf node
        return Node(value=leaf_value)
    
    def get_best_split(self, dataset, num_samples, num_features):
        # dictionary to store the best split
        best_split = {}
        max_var_red = -float("inf")
        # loop over all the features
        for feature_index in range(num_features):
            feature_values = dataset[:, feature_index]
            possible_thresholds = np.unique(feature_values)
            # loop over all the feature values present in the data
            for threshold in possible_thresholds:
                # get current split
                dataset_left, dataset_right = self.split(dataset, feature_index, threshold)
                # check if childs are not null
                if len(dataset_left)>0 and len(dataset_right)>0:
                    y, left_y, right_y = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]
                    # compute information gain
                    curr_var_red = self.variance_reduction(y, left_y, right_y)
                    # update the best split if needed
                    if curr_var_red>max_var_red:
                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["var_red"] = curr_var_red
                        max_var_red = curr_var_red
                        
        # return best split
        return best_split
    
    def split(self, dataset, feature_index, threshold):
        dataset_left = np.array([row for row in dataset if row[feature_index]<=threshold])
        dataset_right = np.array([row for row in dataset if row[feature_index]>threshold])
        return dataset_left, dataset_right
    
    def variance_reduction(self, parent, l_child, r_child):
        weight_l = len(l_child) / len(parent)
        weight_r = len(r_child) / len(parent)
        reduction = np.var(parent) - (weight_l * np.var(l_child) + weight_r * np.var(r_child))
        return reduction
    
    def calculate_leaf_value(self, Y):
        val = np.mean(Y)
        return val
                
    def print_tree(self, tree=None, indent=" "):
        if not tree:
            tree = self.root

        if tree.value is not None:
            print(tree.value)

        else:
            print("X_"+str(tree.feature_index), "<=", tree.threshold, "?", tree.var_red)
            print("%sleft:" % (indent), end="")
            self.print_tree(tree.left, indent + indent)
            print("%sright:" % (indent), end="")
            self.print_tree(tree.right, indent + indent)
    
    def fit(self, X, Y):
        dataset = np.concatenate((X, Y), axis=1)
        self.root = self.build_tree(dataset)
        
    def make_prediction(self, x, tree):
        if tree.value!=None: return tree.value
        feature_val = x[tree.feature_index]
        if feature_val<=tree.threshold:
            return self.make_prediction(x, tree.left)
        else:
            return self.make_prediction(x, tree.right)
    
    def predict(self, X):
        preditions = [self.make_prediction(x, self.root) for x in X]
        return preditions





############################################################
#code below works for decision tree classifier
# class Node:
#     def __init__(self, feature = None, threshold = None, left = None, right = None, *, value=None):
#         self.feature = feature
#         self.threshold = threshold
#         self.left =left
#         self.right = right
#         self.value = value

#     def is_leaf_node(self):
#         return self.value is not None

# class DecisionTree:
#     def __init__(self, min_samples_split = 2, max_depth = 100, n_features = None ):
#         self.min_samples_split = min_samples_split
#         self.max_depth = max_depth
#         self.n_features = n_features
#         self.root = None

#     def fit(self, X, y):
#         self.n_features = X.shape[1] if not self.n_features else min(X.shape[1], self.n_features)
#         self.root = self._grow_tree(X, y)


#     def _grow_tree(self, X, y, depth = 0):
#         n_samples, n_feats = X.shape
#         n_lables = len(np.unique(y))       
        
#         #check the stopping criteria
#         if (depth >= self.max_depth or n_lables == 1 or n_samples < self.min_samples_split):
#             leaf_value = self._most_common_label(y)
#             return Node(value =leaf_value)

#         feat_idxs = np.random.choice(n_feats, self.n_features, replace = False)

#         #find the best split
#         best_feature, best_thres = self._best_split(X, y, feat_idxs)

#         #create child notes
#         left_idxs, right_idxs = self._split(X[:, best_feature], best_thres)
#         left = self._grow_tree(X[left_idxs, :], y[left_idxs], depth + 1)
#         right = self._grow_tree(X[right_idxs, :], y[right_idxs], depth + 1)
#         return Node(best_feature, best_thres, left, right)


#     def _best_split(self, X, y, feat_idxs):
#         best_gain = -1
#         split_idx, split_threshold = None, None

#         for feat_idx in feat_idxs:
#             X_column = X[:, feat_idx]
#             thresholds = np.unique(X_column)

#             for thr in thresholds:
#                 #calculate the information gain
#                 gain = self._information_gain(y, X_column, thr)

#                 if gain > best_gain:
#                     best_gain = gain
#                     split_idx = feat_idx
#                     split_threshold = thr
#         return split_idx, split_threshold

#     def _information_gain(self, y, X_column, threshold):
#         #parent entropy
#         parent_entropy = self._entropy(y)
#         #create children
#         left_idxs, right_idxs = self._split(X_column, threshold)

#         if len(left_idxs) == 0 or len(right_idxs) == 0:
#             return 0

#         #calculate the weighted avg. entropy of children
#         n = len(y)
#         n_l, n_r = len(left_idxs), len(right_idxs)
#         e_l, e_r = self._entropy(y[left_idxs]),self._entropy(y[right_idxs])
#         child_entropy = (n_l/n) * e_l + (n_r/n)*e_r

#         #calculate the IG
#         information_gain = parent_entropy - child_entropy
#         return information_gain
    


#     def _split(self, X_column, split_threshold):
#         left_idxs = np.argwhere(X_column <= split_threshold).flatten()
#         right_idxs = np.argwhere(X_column > split_threshold).flatten()
#         return left_idxs, right_idxs

#     def _entropy(self, y):
#         hist = np.bincount(y)
#         ps = hist/len(y)
        
#         return -np.sum([p*np.log2(p) for p in ps if p>0])


#     def _most_common_label(self, y):
#         counter = Counter(y)
#         value = counter.most_common(1)[0][0]
#         return value
    
#     def predict(self, X):
#         return np.array([self._traverse_tree(x, self.root) for x in X])

#     def _traverse_tree(self, x, node):
#         if node.is_leaf_node():
#             return node.value
#         if x[node.feature] <= node.threshold:
#             return self._traverse_tree(x, node.left)
#         return self._traverse_tree(x, node.right)