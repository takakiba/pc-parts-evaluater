import os
import datetime
import pandas as pd
pd.options.plotting.backend = 'plotly'

csv_passmark = 'CPU_passmark_scores.csv'
csv_price    = 'CPU_prices.csv'

csv_output = 'CPU_value_performances.csv'
html_output_prefix = 'CPU_value_performance'



if __name__ == '__main__':

    ### Show the date info when data are updated
    update_time_pm = datetime.datetime.fromtimestamp(os.path.getmtime(csv_passmark))
    update_time_pr = datetime.datetime.fromtimestamp(os.path.getmtime(csv_price))
    print('Passmark data last updated on {0}'.format(update_time_pm.strftime('%Y/%m/%d %H:%M:%S')))
    print('Price    data last updated on {0}'.format(update_time_pr.strftime('%Y/%m/%d %H:%M:%S')))

    ### read saved csv data
    df_pm = pd.read_csv(csv_passmark)
    df_pr = pd.read_csv(csv_price)

    ### format for pasmark database expression
    df_pr['Chip'] = df_pr['Vender'] + ' ' + df_pr['Chip']
    df_pr['Chip'] = df_pr['Chip'].str.replace('-', ' ')
    # print(df_pm)

    cpu_list   = []
    price_list = []
    score_list = []
    vender_list= []

    for item in df_pr['Chip']:
        cpu_name = item.split('(')[0] 
        if cpu_name in df_pm['Chip'].tolist():
            price = df_pr[df_pr['Chip'] == item]['Price'].values[0]
            score = df_pm[df_pm['Chip'] == cpu_name]['Passmark score'].values[0]
            vender = df_pr[df_pr['Chip'] == item]['Vender'].values[0]

            cpu_list.append(cpu_name)
            price_list.append(price)
            score_list.append(score)
            vender_list.append(vender)
        else:
            print('{0} is not in Passmark data'.format(cpu_name))

    df = pd.DataFrame({'CPU': cpu_list, 'Price':price_list, 'Passmark score':score_list, 'Vender': vender_list})
    df['Value performance'] = df['Passmark score'] / df['Price']
    df.sort_values(['Vender', 'Passmark score'], ascending=False, ignore_index=True, inplace=True)
    # print(df)

    df.to_csv(csv_output)

    fig = df.plot.scatter(x='Price', y='Passmark score', color='Vender', hover_data='CPU')
    fig.show()

    fig.write_html('{0}_{1}.html'.format(html_output_prefix, update_time_pr.strftime('%Y-%m-%d')))


