import os
import datetime
import pandas as pd
pd.options.plotting.backend = 'plotly'

csv_passmark = 'GPU_3Dmark_scores.csv'
csv_price    = 'GPU_prices.csv'

csv_output = 'GPU_value_performances.csv'
html_output_prefix = 'GPU_value_performance'



if __name__ == '__main__':

    ### Show the date info when data are updated
    update_time_pm = datetime.datetime.fromtimestamp(os.path.getmtime(csv_passmark))
    update_time_pr = datetime.datetime.fromtimestamp(os.path.getmtime(csv_price))
    print('Passmark data last updated on {0}'.format(update_time_pm.strftime('%Y/%m/%d %H:%M:%S')))
    print('Price    data last updated on {0}'.format(update_time_pr.strftime('%Y/%m/%d %H:%M:%S')))

    ### read saved csv data
    df_pm = pd.read_csv(csv_passmark, index_col=0)
    df_pr = pd.read_csv(csv_price, index_col=0)

    # print(df_pr)

    ### collect gpu chip list without duplication
    gpu_chip_list = []
    for chip in df_pr['Chip']:
        if chip not in gpu_chip_list:
            gpu_chip_list.append(chip)
    ### collect gpu price: minimum, maximum and average
    gpu_price_info = []
    for chip in gpu_chip_list:
        df_gpu = df_pr[df_pr['Chip'] == chip]
        gpu_price_info.append(
                {'Min': df_gpu['Price'].min(),
                 'Ave': df_gpu['Price'].mean(),
                 'Max': df_gpu['Price'].max()}
                )

    # print(gpu_chip_list)

    ### prepare list to store information needed for plots
    gpu_plots   = []
    score_plots = []
    price_min   = []
    price_ave   = []
    price_max   = []
    venders     = []

    for chip, prices in zip(gpu_chip_list, gpu_price_info):
        ### if benchmark data is available, store data for plots
        if chip in df_pm['GPU name'].to_list():
            score = df_pm[df_pm['GPU name'] == chip]['3DMark score'].values[0]
            # print(chip, score)

            gpu_plots.append(chip)
            score_plots.append(score)
            price_min.append(prices['Ave'] - prices['Min'])
            price_ave.append(prices['Ave'])
            price_max.append(prices['Max'] - prices['Ave'])
            venders.append(chip.split()[0])

    ### create dataframe for plot and save
    df = pd.DataFrame({
        'GPU': gpu_plots,
        'Scores': score_plots,
        'Mean price': price_ave,
        'Eminus_price': price_min,
        'Eplus_price': price_max,
        'Vender' : venders
        })

    ### save dataframe for later reference
    df.sort_values(['Vender', 'Scores'], ascending=False, ignore_index=True, inplace=True)
    df.to_csv(csv_output)

    ### plot dataframe: price versus benchmark score
    # print(df)
    fig = df.plot.scatter(
        x='Mean price', y='Scores', 
        color='Vender', color_discrete_map = {'Intel': '#1E90FF', 'AMD': '#FF6347', 'NVIDIA': '#228B22'},
        hover_data='GPU', 
        error_x='Eplus_price', error_x_minus='Eminus_price'
        )
    fig.show()
    fig.write_html('{0}_{1}.html'.format(html_output_prefix, update_time_pr.strftime('%Y-%m-%d')))



