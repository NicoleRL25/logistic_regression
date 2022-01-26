# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 19:05:57 2022

@author: nmatt
"""

# import data vis modules
import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
from matplotlib.gridspec import GridSpec
import seaborn as sns



def get_promo_rate_by_group(df, group):
    """
    returns DataFrame with counts and promo rate by group
    """
    df = df.copy()
    try:
        promo_by_group = df.groupby([group,'is_promoted'])['employee_id'].count().unstack('is_promoted').reindex()
        promo_by_group['promo_rate'] = promo_by_group[1].div(promo_by_group[0]+promo_by_group[1])
        
        if group in ['awards_won', 'high_performer']:
            promo_by_group.rename({1:'yes', 0:'no'}, inplace = True)
        
    except Exception as e:
        print(e)
    
    return promo_by_group



def plot_promo_demographics(df, group):

    try:
        fig3 = plt.figure(figsize = (15,6))
        fig3.suptitle(f'Promotion Rate by Group: {group}')

        gs = GridSpec(2, 4, width_ratios=[1, 1, 1, 1], height_ratios=[2.5, 2.5])
        ax1 = fig3.add_subplot(gs[0,0])
        ax2 = fig3.add_subplot(gs[0,1], sharey = ax1)
        ax3 = fig3.add_subplot(gs[0,2], sharey = ax1)
        ax4 = fig3.add_subplot(gs[0,3], sharey = ax1)
        ax5 = fig3.add_subplot(gs[1,:-1])
        ax6 = fig3.add_subplot(gs[1,-1], sharey = ax5)

        get_promo_rate_by_group(df, 'gender')[[1,0]].plot.bar(stacked = True, legend = None, 
                                                               color = {1:'lightseagreen', 0:'lightgray'},
                                                           rot = 0, title = 'Gender', xlabel = '', ax = ax1)
        
        get_promo_rate_by_group(df, 'tenure_bands')[[1,0]].plot.bar(stacked = True, legend = None, 
                                                               color = {1:'lightseagreen', 0:'lightgray'},
                                                           rot = 0, title = 'Tenure', xlabel = '', ax = ax2)
                                              
        get_promo_rate_by_group(df, 'awards_won')[[1,0]].plot.bar(stacked = True, legend = None,
                                                                  color = {1:'lightseagreen', 0:'lightgray'},
                                                           rot = 0, title = 'Awards Won', xlabel = '', ax = ax3)
        get_promo_rate_by_group(df, 'high_performer')[[1,0]].plot.bar(stacked = True, title = 'High Performer',
                                                               xlabel = '', 
                                                                      color = {1:'lightseagreen', 0:'lightgray'},
                                                           rot = 0, ax = ax4)
        handles, labels = ax4.get_legend_handles_labels()
        labels = ['promoted' if l == '1' else 'not promoted' for l in labels]
        ax4.legend(labels, frameon = False, loc = 'upper right', bbox_to_anchor = (1.5, 1.1))
        
        get_promo_rate_by_group(df, 'region_grps')[[1,0]].plot.bar(stacked = True, legend = None, xlabel = '',
                                                                   color = {1:'lightseagreen', 0:'lightgray'},
                                                           rot = 0, title = 'Top Regions', ax = ax5)

        get_promo_rate_by_group(df, 'age_group')[[1,0]].plot.bar(stacked = True, legend = None, xlabel= '', 
                                                                color = {1:'lightseagreen', 0:'lightgray'},
                                                           rot = 0, title = 'Generations', ax = ax6)



        for ax in fig3.axes:
            for spine in ['top', 'right']:
                ax.spines[spine].set_visible(False)

            for spine in ['bottom', 'left']:
                ax.spines[spine].set_position(('outward', 5))


            ax.tick_params(bottom = False, left = False)
            
            ax.grid(axis = 'y')

            for p in ax.containers[-1].patches:
                height = p.get_height()
                width = p.get_width()
                promos = p.get_y()
                x = p.get_x()
                total = promos + height
                promo_rate = promos/total

                ax.annotate(f'{promo_rate:0.0%}', xy = (x,promos), 
                            xytext = (x+width/2,promos), va='bottom',
                            ha = 'center') 
                

        plt.tight_layout()
    
    except Exception as e:
        print(e)
        
        
        
def plot_fitted_values(labels, pct_promoted):
    
    pct_not_promoted = 1- pct_promoted
    
    fig, ax = plt.subplots()

    ax.barh(labels, pct_promoted, height = 0.5, label='% promoted', 
            color = 'lightseagreen')
    
    ax.barh(labels, pct_not_promoted, height= 0.5, left=pct_promoted, 
            label='% not promoted', color = 'lightgray')

    ax.set_title('Promotion Rate by Group', loc = 'left', pad = 30)
    ax.legend(frameon = False, ncol = 2, loc = 'upper left', 
              bbox_to_anchor = (0,1.12))
    ax.xaxis.set_visible(False)

    for spine in ax.spines:
        ax.spines[spine].set_visible(False)

    ax.tick_params(left = False, bottom = False)


    for con in ax.containers:

        for patch in con.patches:
            x = patch.get_x()
            y = patch.get_y()
            width = patch.get_width()
            height = patch.get_height()

            if width > 0:    
                ax.annotate(f'{width:0.0%}', xy=(x + width/2,y + height/2), 
                            ha='center', va = 'center')


def plot_headcount_by_dept(df):
    # plot of headcount by department
    
    fig, ax = plt.subplots()
    df.department.value_counts(dropna = False).sort_values().plot.barh(color = '#4285F4', ax = ax)
    for p in ax.patches: # annotates each patch with the department hc
        width = p.get_width() # gets width of bar; headcount
        y = p.get_y()
        ax.annotate(f'{width:0,.0f}', xy = (width,y), va='bottom') 
        
    ax.tick_params(bottom = False, left = False) # removes tick marks from x and y-axis
    
    # removes all spines except left
    for spine in ['right', 'top', 'bottom']:
        ax.spines[spine].set_visible(False)
            
    ax.spines['left'].set_position(('outward',10))
    ax.xaxis.set_visible(False)
    ax.set_title('Headcount by Department', loc = 'left', pad = 10)
    
    
    
    return fig, ax
    

def plot_promos_by_dept(promos_by_dept, size_order):
    # plots promoted vs. not-promoted by department
    fig1, ax1 = plt.subplots()
    
    # plots stacked bar chart
    (promos_by_dept.reindex(size_order).reindex([1,0], axis = 1)
     .plot.barh(stacked = True, 
                color = {1:'lightseagreen',0:'lightgray'}, 
                legend = None, ax = ax1))
    
    # annotates the promotion rate for each department
    for p in ax1.containers[-1].patches:
        width = p.get_width()
        promos = p.get_x()
        y = p.get_y()
        total = promos + width
        promo_rate = promos/total
        
        ax1.annotate(f'{promo_rate:0.0%}', xy = (promos,y), va='bottom') 
        
    ax1.tick_params(bottom = False, left = False) # removes tick marks from x and y-axis    
        
    # removes all spines except left
    for spine in ['right', 'top']:
        ax1.spines[spine].set_visible(False)
            
    for spine in ['left', 'bottom']:
        ax1.spines[spine].set_position(('outward',10))            
    
    ax1.set_title('Promo Rates by Department', loc = 'left', pad = 10)    
    handles, labels = ax1.get_legend_handles_labels()
    labels = ['promoted' if l == '1' else 'not promoted' for l in labels]
    ax1.legend(labels, ncol = 2, frameon = False, loc = 'upper left',
               bbox_to_anchor = (0,1.1))
    
    return fig1, ax1



def plot_observed_vs_expected(promos_by_dept_fitted):
    
# plots observed vs expected values by department

    fig2, ax2 = plt.subplots()
    promos_by_dept_fitted.plot.barh(color = {'observed':'orange',
                                             'expected':'#4285F4'}, ax = ax2)
    ax2.set_title('Promotions: Observed vs. Expected', loc = 'left', pad = 20)
    
    # removes top and right spines
    for spine in ['right', 'top']:
        ax2.spines[spine].set_visible(False)
    
        # sets left and bottom spines outward
    for spine in ['left', 'bottom']:
        ax2.spines[spine].set_position(('outward',10))
    
    # removes tick params and y-label    
    ax2.tick_params(bottom = False, left = False)
    ax2.set_ylabel('')
    
    #moves legend below title
    ax2.legend(ncol = 2, frameon = False, loc = 'upper left', 
               bbox_to_anchor = (0,1.1))
    
    
    return fig2, ax2

    
                