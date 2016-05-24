from config import *
import pandas as pd
import os

from sklearn.metrics import precision_recall_fscore_support
from scipy import sparse

gold = pd.read_table(GOLD)
gold_dict = gold.groupby(['collection_id', 'file_id']).groups
tags = list(set(gold.tag))
ids = list(set(gold_dict))

def dict2sparse(d):
    out = sparse.lil_matrix((len(ids), max(tags)+1))
    g = d.groupby(['collection_id', 'file_id']).groups
    for cf, ts in g.iteritems():
        for t in ts:
            try:
                out[ids.index(cf), d.tag[t]] = True
            except Exception as e:
                print t
                # raise e
    return out

y_true = dict2sparse(gold)

def get_scores():
    submissions = {}
    for team in LOGINS:
        fdir = os.path.join(UPLOAD_FOLDER, team)
        submissions[team] = {}
        for fname in os.listdir(fdir):
            sub = pd.read_table(os.path.join(fdir,fname), converters={0:int, 1:int,2:int})
            print sub.dtypes
            if len(set(list(sub.columns)) & set(['collection_id', 'file_id', 'tag'])):
                y_pred = dict2sparse(sub)
                score = precision_recall_fscore_support(y_true, y_pred, average='micro')
                submissions[team][fname] = score
            else:
                print sub.columns
    return submissions

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cStringIO

def plot_scores(scores):
    f, ax = plt.subplots()
    ax.set_title('Precision-Recall curve')
    ax.set_xlim([0.0, 1])
    ax.set_ylim([0.0, 1])
    ax.set_xlabel('Recall')
    ax.set_ylabel('Precision')
    ps,rs = zip(*PR)
    ax.plot(rs, ps)

    for team,teamsubs in scores.iteritems():
        for sub, scores in teamsubs.iteritems():
            p,r,_,_ = scores
            ax.annotate(sub,
                xy=(r,p),
                xytext=(r+0.05,p+0.05),
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='left',
                verticalalignment='bottom',
                # clip_on=True,  # clip to the axes bounding box
                )

    imgbuf = cStringIO.StringIO()
    f.savefig(imgbuf,format='png',bbox_inches='tight')
    imgbuf.seek(0)
    code = imgbuf.getvalue().encode("base64").strip()
    return "data:image/png;base64,%s" % code


PR = [(0.000917, 0.975),(0.00163, 0.960),(0.00211, 0.947),(0.00256, 0.937),(0.00294, 0.928),(0.00334, 0.919),(0.00370, 0.911),(0.00401, 0.904),(0.00424, 0.899),(0.00448, 0.893),(0.00479, 0.886),(0.00490, 0.884),(0.00512, 0.879),(0.00531, 0.875),(0.00554, 0.86),(0.00577, 0.864),(0.00592, 0.862),(0.00620, 0.855),(0.00637, 0.851),(0.00656, 0.846),(0.00671, 0.842),(0.0068, 0.839),(0.00712, 0.832),(0.00718, 0.831),(0.00724, 0.830),(0.00735, 0.827),(0.00757, 0.822),(0.00774, 0.818),(0.00787, 0.8),(0.00802, 0.812),(0.0081, 0.809),(0.00829, 0.806),(0.00847, 0.802),(0.00874, 0.79),(0.00889, 0.793),(0.00900, 0.790),(0.00912, 0.787),(0.00922, 0.785),(0.00925, 0.785),(0.00934, 0.782),(0.00949, 0.778),(0.00962, 0.774),(0.00970, 0.773),(0.00976, 0.771),(0.00983, 0.77),(0.00994, 0.767),(0.0100, 0.764),(0.0102, 0.761),(0.0102, 0.760),(0.0104, 0.757),(0.0105, 0.755),(0.0106, 0.753),(0.0107, 0.749),(0.0108, 0.745),(0.0109, 0.743),(0.0110, 0.74),(0.0111, 0.73),(0.0112, 0.736),(0.0113, 0.733),(0.0116, 0.728),(0.0117, 0.72),(0.0118, 0.723),(0.0118, 0.721),(0.0119, 0.720),(0.0119, 0.718),(0.0120, 0.717),(0.0120, 0.716),(0.0121, 0.713),(0.0122, 0.712),(0.0122, 0.71),(0.0123, 0.707),(0.0124, 0.706),(0.012, 0.701),(0.0127, 0.699),(0.0128, 0.694),(0.0130, 0.689),(0.0131, 0.686),(0.0133, 0.683),(0.0133, 0.681),(0.013, 0.676),(0.0136, 0.675),(0.013, 0.67),(0.0137, 0.672),(0.0138, 0.670),(0.01, 0.666),(0.0140, 0.664),(0.0141, 0.662),(0.0141, 0.660),(0.0143, 0.658),(0.0144, 0.655),(0.0144, 0.653),(0.0145, 0.651),(0.0146, 0.647),(0.0148, 0.643),(0.0149, 0.6),(0.0149, 0.638),(0.0150, 0.636),(0.0151, 0.633),(0.0151, 0.630),(0.0152, 0.628),(0.0153, 0.625),(0.0155, 0.620),(0.0155, 0.618),(0.0156, 0.616),(0.0159, 0.6),(0.016, 0.606),(0.0160, 0.603),(0.0161, 0.60),(0.0162, 0.59),(0.016, 0.594),(0.0164, 0.591),(0.0164, 0.588),(0.0165, 0.584),(0.0167, 0.578),(0.0168, 0.57),(0.016, 0.571),(0.0169, 0.568),(0.017, 0.564),(0.0171, 0.560),(0.0172, 0.557),(0.0174, 0.551),(0.0177, 0.542),(0.0179, 0.536),(0.0180, 0.533),(0.018, 0.522),(0.0185, 0.519),(0.0186, 0.516),(0.0187, 0.512),(0.0188, 0.50),(0.0189, 0.504),(0.0191, 0.50),(0.0192, 0.497),(0.0193, 0.493),(0.0194, 0.488),(0.0196, 0.479),(0.0197, 0.474),(0.0199, 0.464),(0.0200, 0.460),(0.0202, 0.456),(0.0202, 0.450),(0.0204, 0.445),(0.0205, 0.44),(0.0206, 0.436),(0.0210, 0.421),(0.021, 0.414),(0.0212, 0.410),(0.0214, 0.40),(0.0215, 0.40),(0.0217, 0.396),(0.0218, 0.390),(0.0221, 0.379),(0.0223, 0.374),(0.0225, 0.369),(0.0226, 0.363),(0.0228, 0.357),(0.0230, 0.352),(0.0231, 0.345),(0.0234, 0.340),(0.0234, 0.333),(0.0237, 0.328),(0.0238, 0.321),(0.0240, 0.315),(0.0242, 0.308),(0.0244, 0.302),(0.0247, 0.296),(0.0250, 0.29),(0.0252, 0.285),(0.0254, 0.277),(0.0257, 0.271),(0.0259, 0.264),(0.0261, 0.256),(0.0267, 0.243),(0.0270, 0.236),(0.0273, 0.229),(0.0276, 0.22),(0.0281, 0.214),(0.0286, 0.208),(0.0289, 0.200),(0.0291, 0.191),(0.0294, 0.182),(0.0299, 0.174),(0.0309, 0.157),(0.0317, 0.150),(0.0323, 0.141),(0.0329, 0.132),(0.0336, 0.122),(0.034, 0.112),(0.0348, 0.101),(0.0350, 0.0892),(0.0351, 0.0768),(0.0359, 0.0654),(0.0373, 0.0543),(0.0373, 0.0407),(0.0381, 0.0277),(0.0383, 0.0139)]