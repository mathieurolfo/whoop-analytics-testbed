def get_transition_probabilities(x,y, window_start = 0, window_end = -1):
    import numpy
    pct_hrv = numpy.percentile(x,50)
    pct_rhr = numpy.percentile(y,50)
    xd = x[window_start:window_end]
    yd = y[window_start:window_end]
    symp_unbalanced = ((xd<pct_hrv) & (yd>pct_rhr))
    psymp_unbalanced = ((xd<pct_hrv) & (yd<pct_rhr))
    balanced = xd>pct_hrv
    balanced_to_balanced = (balanced[:-1]==True) & (balanced[1:]==True)
    balanced_to_symp = (balanced[:-1]==True) & (symp_unbalanced[1:]==True)
    balanced_to_psymp = (balanced[:-1]==True) & (psymp_unbalanced[1:]==True)
    symp_to_balanced = (symp_unbalanced[:-1]==True) & (balanced[1:]==True)
    symp_to_symp = (symp_unbalanced[:-1]==True) & (symp_unbalanced[1:]==True)
    symp_to_psymp = (symp_unbalanced[:-1]==True) & (psymp_unbalanced[1:]==True)
    psymp_to_balanced = (psymp_unbalanced[:-1]==True) & (balanced[1:]==True)
    psymp_to_symp = (psymp_unbalanced[:-1]==True) & (symp_unbalanced[1:]==True)
    psymp_to_psymp = (psymp_unbalanced[:-1]==True) & (psymp_unbalanced[1:]==True)
    denom = balanced.sum()+symp_unbalanced.sum()+psymp_unbalanced.sum()
    return {
    'balanced_to_balanced' : balanced_to_balanced.sum()/balanced.sum(),
    'balanced_to_symp' : balanced_to_symp.sum()/balanced.sum(),
    'balanced_to_psymp' : balanced_to_psymp.sum()/balanced.sum(),
    'symp_to_balanced' : symp_to_balanced.sum()/symp_unbalanced.sum(),
    'symp_to_symp' : symp_to_symp.sum()/symp_unbalanced.sum(),
    'symp_to_psymp' : symp_to_psymp.sum()/symp_unbalanced.sum(),
    'psymp_to_balanced' : psymp_to_balanced.sum()/psymp_unbalanced.sum(),
    'psymp_to_psymp' : psymp_to_psymp.sum()/psymp_unbalanced.sum(),
    'psymp_to_symp': psymp_to_symp.sum()/psymp_unbalanced.sum(),
    'occupation_rates': [balanced.sum()/denom,psymp_unbalanced.sum()/denom,symp_unbalanced.sum()/denom],
    }
def make_transition_plots(keydata, interval=30):
    import numpy
    import matplotlib.pyplot as plt
    x = keydata['recovery.heartRateVariabilityRmssd'].values
    y = keydata['recovery.restingHeartRate'].values
    max_day = len(x) -interval -1
    dates = keydata['day'].values[:max_day]
    dates = [x.split('-')[1:] for x in dates]
    dates = numpy.array([str(x[0])+'-'+str(x[1]) for x in dates])
    ticks = dates[list(range(0,len(dates),30))]
    plt.clf()
    plt.figure(figsize=(15,10))
    plt.subplot(3,4,1)
    plt.scatter(dates,
                [get_transition_probabilities(x,y,i,i+interval)['symp_to_psymp'] for i in range(max_day)],alpha=.75)
    plt.ylabel('transition probability')
    plt.title('Symp -> Psymp')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,2)
    plt.scatter(dates,
                [get_transition_probabilities(x,y,i,i+interval)['symp_to_balanced'] for i in range(max_day)],alpha=.75)
    plt.ylabel('transition probability')
    plt.title('Symp -> Balanced')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,3)
    plt.scatter(dates,
                [get_transition_probabilities(x,y,i,i+interval)['symp_to_symp'] for i in range(max_day)],alpha=.75)
    plt.ylabel('transition probability')
    plt.title('Symp -> Symp')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,5)
    plt.scatter(dates,
                [get_transition_probabilities(x,y,i,i+interval)['psymp_to_psymp'] for i in range(max_day)],alpha=.75)
    plt.ylabel('transition probability')
    plt.title('Psymp -> Psymp')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,6)
    plt.scatter(dates,
                [get_transition_probabilities(x,y,i,i+interval)['psymp_to_balanced'] for i in range(max_day)],alpha=.75)
    plt.ylabel('transition probability')
    plt.title('Psymp -> Balanced')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,7)
    plt.scatter(dates,
                [get_transition_probabilities(x,y,i,i+interval)['psymp_to_symp'] for i in range(max_day)],alpha=.75)
    plt.ylabel('transition probability')
    plt.title('Psymp -> Symp')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,9)
    plt.scatter(dates,
                [get_transition_probabilities(x,y,i,i+interval)['balanced_to_psymp'] for i in range(max_day)],alpha=.75)
    plt.ylabel('transition probability')
    plt.title('Balanced -> Psymp')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,10)
    plt.scatter(dates,
                [get_transition_probabilities(x,y,i,i+interval)['balanced_to_balanced'] for i in range(max_day)],alpha=.75)
    plt.ylabel('transition probability')
    plt.title('Balanced -> Balanced')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,11)
    plt.scatter(dates,
                [get_transition_probabilities(x,y,i,i+interval)['balanced_to_symp'] for i in range(max_day)],alpha=.75)
    plt.ylabel('transition probability')
    plt.title('Balanced -> Symp')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,4)
    plt.scatter(dates, [get_transition_probabilities(x,y,i,i+interval)['occupation_rates'][2] for i in range(max_day)],alpha=.75)
    plt.ylabel('occupation probability')
    plt.title('Symp')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,8)
    plt.scatter(dates, [get_transition_probabilities(x,y,i,i+interval)['occupation_rates'][1] for i in range(max_day)],alpha=.75)
    plt.ylabel('occupation probability')
    plt.title('Psymp')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.subplot(3,4,12)
    plt.scatter(dates, [get_transition_probabilities(x,y,i,i+interval)['occupation_rates'][0] for i in range(max_day)],alpha=.75)
    plt.ylabel('occupation probability')
    plt.title('Balanced')
    plt.xlabel('day')
    plt.ylim(0,1.05)
    plt.xticks(ticks)
    plt.tight_layout()
    plt.show()
