# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from tqdm import tqdm
import pandas as pd
import numpy as np

class Concurrent:
    def __init__(self, n_pro, func, *args):
        self.n_pro = n_pro
        self.q_in = Queue(maxsize=-1)
        self.q_out = Queue(maxsize=-1)
        self.counter = 0
        self.p_list = []
        for i in range(self.n_pro):
            p = Process(func, self.q_in, self.q_out, *args, daemon=True)
            self.p_list.append(p)
            p.start()
    def put(self, input_list):
        for input in input_list:
            self.q_in.put(input)
            self.counter += 1
    def get(self):
        while self.check():
            try:
                output = self.q_out.get(timeout=1)
                self.counter -= 1
                return output
            except:
                continue
    def check(self):
        if sum([0 if p.alive() else 1 for p in self.p_list]) > 0:
            self.exit()
            raise('RuntimeError')
        return True
    def empty(self):
        return True if self.counter == 0 else False
    def overload(self):
        return True if self.counter >= self.n_pro else False
    def exit(self):
        self.q_out.close()
        for p in self.p_list:
            p.terminate()
            p.join()
    def __del__(self):
        self.exit()

def feature_processing(data, var_list , min_value=-np.inf, max_value=np.inf, fill_else=-9999, decimal=3):
    def limit(x):
        return x if x >= min_value and x <= max_value else fill_else
    for var in tqdm(var_list):
        data[var] = data[var].astype('float').apply(limit).round(decimal)

def target_processing(data, target_region, fill_na=0, fill_else=np.nan):
    for target in tqdm(list(target_region.keys())):
        data[target].fillna(fill_na,inplace=True)
        data.loc[~data.query(target_region[target]).index, target] = fill_else

def define_index(data, counter, target_list, sample_weight):
    index_list = ['cnt']
    data['cnt'] = (data[counter] >= 0) * 1
    for target in target_list:
        index_list += ['cnt_%s' % target, 'sum_%s' % target]
        if target in sample_weight.keys():
            weight = sample_weight[target]
            if type(weight) == str:
                data['cnt_%s' % target] = (data[target] >= 0) * data[weight]
                data['sum_%s' % target] = (data[target] >= 0) * data[weight] * data[target]
            else:
                data['cnt_%s' % target] = (data[target] >= 0) * data[weight[0]]
                data['sum_%s' % target] = (data[target] >= 0) * data[weight[1]] * data[target]
        else:
            data['cnt_%s' % target] = (data[target] >= 0) * 1
            data['sum_%s' % target] = (data[target] >= 0) * data[target]
    return index_list

def evaluate_gap(data, target_list, target_min_dict, target_max_dict, target_weight, method):
    for target in target_list:
        data['avg_%s' % target] = data['sum_%s' % target] / data['cnt_%s' % target]
        data['gap_%s' % target] = 0
        if target in target_min_dict.keys():
            data['gap_%s' % target] += (data['avg_%s' % target] - target_min_dict[target]) * (data['avg_%s' % target] > target_min_dict[target])
        if target in target_max_dict.keys():
            data['gap_%s' % target] += (target_max_dict[target] - data['avg_%s' % target]) * (data['avg_%s' % target] < target_max_dict[target])
        data['gap_%s' % target] = data['gap_%s' % target] * (target_weight[target] if target in target_weight.keys() else 1)
    data['gap'] = data[['gap_%s' % target for target in target_list]].apply(method, axis=1)
    return data['gap']

def single_cutting(data, var, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None):
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    index_list = define_index(data, counter, target_list, sample_weight)
    data['value'] = data.eval(var).round(3)
    grouped = data.groupby(by='value',as_index=False)[index_list].sum()
    ascending_list = [ascending] if ascending else [True, False]
    result = pd.DataFrame()
    for ascending in ascending_list:
        temp = grouped.sort_values(by='value',ascending=ascending)
        temp['direction'] = '<' if ascending == True else '>'
        temp['cutoff'] = (temp['value'] + temp['value'].shift(-1)) / 2
        temp[index_list] = temp[index_list].cumsum()
        temp['gap'] = evaluate_gap(temp, target_list, target_min_dict, target_max_dict, target_weight, method)
        result = result.append(temp,ignore_index=True)
    result = result[result['cnt'] >= cnt_req].sort_values(by='cnt',ascending=True).drop_duplicates(subset='direction',keep='first')
    result = result[-np.isnan(result['cutoff'])]
    cutoff = result.sort_values(by='gap',ascending=True).iloc[:1]
    cutoff['var'] = var
    return cutoff

def couple_cutting(data, var_couple, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None, pct_single=0):
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    index_list = define_index(data, counter, target_list, sample_weight)
    var1, var2 = var_couple[1], var_couple[2]
    data['value1'] = data.eval(var1).round(3)
    data['value2'] = data.eval(var2).round(3)
    mesh = pd.merge(data[['cnt','value1']].drop_duplicates(), data[['cnt','value2']].drop_duplicates(), how='inner', on=['cnt'])[['value1','value2']]
    grouped = mesh.merge(data.groupby(by=['value1','value2'],as_index=False)[index_list].sum(), how='left', on=['value1','value2']).fillna(0)
    ascending_list = [(ascending,ascending)] if ascending else [(True,True),(True,False),(False,True),(False,False)]
    result = pd.DataFrame()
    for ascending in ascending_list:
        temp = grouped.sort_values(by='value1',ascending=ascending[0])
        temp['direction1'] = '<' if ascending[0] == True else '>'
        temp['direction2'] = '<' if ascending[1] == True else '>'
        temp['cutoff1'] = (temp['value1'] + temp.groupby(by='value2')['value1'].shift(-1)) / 2
        temp[index_list] = temp.groupby(by='value2')[index_list].cumsum()
        temp = temp.sort_values(by='value2',ascending=ascending[1])
        temp['cutoff2'] = (temp['value2'] + temp.groupby(by='value1')['value2'].shift(-1)) / 2
        temp[index_list] = temp.groupby(by='value1')[index_list].cumsum()
        temp1 = grouped.groupby(by='value1',as_index=False)['cnt'].sum()
        temp1.sort_values(by='value1',ascending=ascending[0],inplace=True)
        temp1['cnt'] = temp1['cnt'].cumsum()
        temp2 = grouped.groupby(by='value2',as_index=False)['cnt'].sum()
        temp2.sort_values(by='value2',ascending=ascending[1],inplace=True)
        temp2['cnt'] = temp2['cnt'].cumsum()
        temp = temp.merge(temp1, how='inner', on='value1', suffixes=('','_1')).merge(temp2, how='inner', on='value2', suffixes=('','_1'))
        temp['pct_1'] = (temp['cnt_2'] - temp['cnt']) / (grouped['cnt'].sum() - temp['cnt'])
        temp['pct_2'] = (temp['cnt_1'] - temp['cnt']) / (grouped['cnt'].sum() - temp['cnt'])
        temp['gap'] = evaluate_gap(temp, target_list, target_min_dict, target_max_dict, target_weight, method)
        result = result.append(temp,ignore_index=True)
    result = result[result['cnt'] >= cnt_req].sort_values(by='cnt',ascending=True).drop_duplicates(subset=['direction1','direction2','value1'],keep='first')
    result = result[(-np.isnan(result['cutoff1'])) & (-np.isnan(result['cutoff2']))]
    result = result[(result['pct_1'] >= pct_single) & (result['pct_2'] >= pct_single)]
    cutoff = result.sort_values(by='gap',ascending=True).iloc[:1]
    cutoff['var1'] = var1
    cutoff['var2'] = var2
    return cutoff

def multiple_cutting(data, var_list, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None, pct_single=0, var_min=5, var_max=10, min_gain=0, n_pro=30):
    def subtask(q_in, q_out, data, var_cutoff, counter, cnt_req, cnt_tol, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, pct_single, var_min, var_max):
        while 1:
            try:
                input = q_in.get(timeout=1)
            except:
                continue
            data['flag'] = 1
            for var in var_cutoff.keys():
                if var not in input:
                    direciton, cutoff = var_cutoff[var]
                    data['flag'] = data['flag'] * ((data[var] < cutoff) if direction == '<' else (data[var] > cutoff))
            if len(input) == 1:
                var = input[0]
                cutoff = single_cutting(data.query('flag == 1'), var, counter, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending)
            else:
                var_couple = (input[0],input[1])
                cutoff = couple_cutting(data.query('flag == 1'), var_couple, counter, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending, pct_single=pct_single)
            var_num = len(set(list(var_cutoff.keys()+input)))
            cutoff['gap_adj'] = cutoff['gap'] + 10 * (cutoff['cnt'] - cnt_req) / cnt_tol + 100 * (var_min - var_num) * (var_num < var_min) + 100 * (var_num - var_max) * (var_num > var_max)
            q_out.put(cutoff)
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    _ = define_index(data, counter, target_list, sample_weight)
    cnt_tol = data['cnt'].sum()
    var_cutoff = {}
    def calculate(input_list):
        con = Concurrent(n_pro, subtask, data, var_cutoff, counter, cnt_req, cnt_tol, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, pct_single, var_min, var_max)
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        con.exit()
        return result
    gap_min = np.inf
    while 1:
        if len(var_cutoff) == 0:
            input_list = [(var,) for var in var_list]
        else:
            input_list = []
            var_list_1 = list(var_cutoff.keys())
            for i,var1 in enumerate(var_list_1):
                input_list += [(var1,var2) for j,var2 in enumerate(var_list_1) if j > i]
                input_list += [(var1,var2) for var2 in var_list if var2 not in var_list_1]
        result = calculate(input_list)
        if not result.empty:
            opt = result.sort_values(by='gap_adj',ascending=True).iloc[0]
            if opt['gap_adj'] > gap_min-min_gain:
                break
            gap_min = opt['gap_adj']
            if 'var' in opt.index:
                var_cutoff[opt['var']] = (opt['direction'],opt['cutoff'])
            else:
                var_cutoff[opt['var1']] = (opt['direction1'],opt['cutoff1'])
                var_cutoff[opt['var2']] = (opt['direction2'],opt['cutoff2'])
        else:
            break
    result = []
    for var in var_cutoff.keys():
        data['cnt1'] = data['cnt']
        for i in var_cutoff.keys():
            if i != var:
                direction, cutoff = var_cutoff[i]
                data['cnt1'] = data['cnt1'] * ((data[i] < cutoff) if direction == '<' else (data[i] > cutoff))
        direction, cutoff = var_cutoff[var]
        data['cnt2'] = data['cnt'] * (data[var] < cutoff) if direction == '<' else (data[var] > cutoff)
        pct_self = (data['cnt'].sum() - data['cnt2'].sum()) / (data['cnt'].sum() - data.eval('cnt1*cnt2').sum())
        pct_gain = (data['cnt1'].sum() - data.eval('cnt1*cnt2').sum()) / (data['cnt'].sum() - data.eval('cnt1*cnt2').sum())
        result.append([var,direction,cutoff,pct_self,pct_gain])
    var_cutoff = pd.DataFrame(columns=['var','direction','cutoff','pct_self','pct_gain'], data=result).sort_values(by='pct_gain',ascending=False).reset_index(drop=True)
    return var_cutoff

def multiple_grouping(data, var_list, counter, tab_conf, sample_weight={}, target_weight={}, method='sum', ascending=False, pct_single=0, var_min=5, var_max=10, min_gain=0, reverse=False, n_pro=30):
    target_min_list = [column.replace('min_','') for column in tab_conf.columns if 'min_' in column]
    target_max_list = [column.replace('max_','') for column in tab_conf.columns if 'max_' in column]
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    tab_copy = tab_conf.sort_values(by='id',ascending=True)
    if reverse == True:
        index_list = [column for column in tab_copy.columns if 'min_' in column or 'max_' in column]
        tab_copy[index_list] = tab_copy[index_list] * tab_copy['pct']
        tab_copy[index_list] = tab_copy[index_list].cumsum()
        tab_copy['pct'] = tab_copy['pct'].cumsum()
        tab_copy[index_list] = tab_copy[index_list] / tab_copy['pct']
        tab_copy.sort_values(by='id',ascending=False,inplace=True)
    index_list = define_index(data, counter, target_list, sample_weight)
    cnt_tol = data['cnt'].sum()
    data_choice = data.copy()
    result = pd.DataFrame()
    for i in range(tab_copy.shape[0]):
        value = tab_copy.iloc[i]
        cnt_req = int(cnt_tol*value['pct'])
        target_min_dict = {}
        for target in target_min_list:
            target_min_dict[target] = value['min_%s' % target]
        target_max_dict = {}
        for target in target_max_list:
            target_max_dict[target] = value['max_%s' % target]
        var_cutoff = multiple_cutting(data_choice, var_list, counter, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending, pct_single=pct_single, var_min=var_min, var_max=var_max, min_gain=min_gain, n_pro=n_pro)
        data_choice['flag'] = 1
        for var in var_cutoff.keys():
            direction, cutoff = var_cutoff[var]
            data_choice['flag'] = data_choice['flag'] * ((data_choice[var] < cutoff) if direction == '<' else (data_choice[var] > cutoff))
        if reverse == True:
            data_choice = data_choice.query('flag == 1')
        else:
            data_choice = data_choice.query('flag == 0')
        result = result.append(var_cutoff,ignore_index=True)
    cross_tab = pd.pivot_table(result, index='id', columns='var', values='cutoff')
    if reverse == True:
        cross_tab.sort_index(ascending=False,inplace=True)
        cross_tab = cross_tab.cummin() if ascending == True else cross_tab.cummax()
    cross_tab['region'] = cross_tab.apply(lambda x : ' and '.join(['%s %s %f' % (column,'<' if ascending == True else '>',x[column]) for column in cross_tab.columns if x[column] > 0]))
    cross_tab = cross_tab.reset_index().sort_values(by='id',ascending=True)
    data['id'] = 0
    for i in range(cross_tab.shape[0]):
        value = cross_tab.iloc[i]
        data.loc[(data['id'] == 0) & (data.index.isin(data.query(value['region']).index)), 'id'] = value['id']
    grouped = data.groupby(by='id',as_index=False)[index_list].sum()
    grouped['pct_group'] = grouped['cnt'] / cnt_tol
    for target in target_list:
        grouped['avg_%s' % target] = grouped['sum_%s' % target] / grouped['cnt_%s' % target]
    result = tab_conf.merge(cross_tab, how='left', on='id').merge(grouped[['id','pct_group']+['avg_%s' % target for target in target_list]], how='left', on='id')
    return result

def grid_cutting(data, var_couple, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=False, min_gain=0, only_gain=True):
    target_list = list(target_min_dict.keys()) + [target for target in target_max_dict.keys() if target not in target_min_dict.keys()]
    index_list = define_index(data, counter, target_list, sample_weight)
    var_x, var_y = var_couple[0], var_couple[1]
    data['bin_x'] = data[var_x].round(3)
    data['bin_y'] = data[var_y].round(3)
    bin_x = list(data['bin_x'].drop_duplicates().sort_values(ascending=ascending))
    bin_y = list(data['bin_y'].drop_duplicates().sort_values(ascending=ascending))
    mesh = pd.merge(pd.DataFrame({'bin_x':bin_x,'flag':1}), pd.DataFrame({'bin_y':bin_y,'flag':1}), how='inner', on='flag')[['bin_x','bin_y']]
    mesh = mesh.merge(data.groupby(by=['bin_x','bin_y'],as_index=False)[index_list].sum(), how='left', on=['bin_x','bin_y']).fillna(0)
    mesh.set_index(['bin_x','bin_y'])
    mesh['flag'] = 0
    choice = {}
    for index in index_list:
        choice[index] = 0
    border = []
    gap_min = np.inf
    while 1:
        if len(border) > 0:
            point_cand = []
            for i,j in enumerate(border):
                if i == 0 and j < len(var_y):
                    point_cand.append((i+1,j+1))
                elif i > 0 and j < border[i-1]:
                    point_cand.append((i+1,j+1))
            else:
                if i < len(bin_x) - 1:
                    point_cand.append((i+2,1))
        else:
            point_cand = [(1,1)]
        if len(point_cand) == 0:
            break
        cand = mesh.loc[[(bin_x[p[0]-1],bin_y[p[1]-1]) for p in point_cand]].reset_index()
        cand['gap_add'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
        for index in index_list:
            cand[index] += choice[index]
        cand['gap_tol'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
        if only_gain:
            opt = cand.sort_values(by='gap_add',ascending=True).iloc[0]
        else:
            opt = cand.sort_values(by='gap_tol',ascending=True).iloc[0]
        if min_gain >= 0 and opt['gap_tol'] > gap_min-min_gain:
            break
        point_x = bin_x.index(opt['bin_x']) + 1
        point_y = bin_y.index(opt['bin_y']) + 1
        if point_x <= len(border):
            border[point_x-1] = point_y
        else:
            border.append(point_y)
        for index in index_list:
            choice[index] = opt[index]
        mesh.loc[(opt['bin_x'],opt['bin_y']), 'flag'] = 1
        if min_gain < 0 and opt['cnt'] >= cnt_req:
            break
    cross_tab = pd.pivot_table(mesh, index='bin_x', columns='bin_y', values='flag')
    return cross_tab

def grid_grouping(data, var_couple, counter, tab_conf, sample_weight={}, target_weight={}, method='sum', ascending=False, reverse=False, min_gain=0, only_gain=True):
    target_min_list = [column.replace('min_','') for column in tab_conf.columns if 'min_' in column]
    target_max_list = [column.replace('max_','') for column in tab_conf.columns if 'max_' in column]
    target_list = target_min_list + [target for target in target_max_list if target not in target_min_list]
    tab_copy = tab_conf.sort_values(by='id',ascending=True)
    if reverse:
        index_list = [column for column in tab_copy.columns if 'min_' in column or 'max_' in column]
        tab_copy[index_list] = tab_copy[index_list] * tab_copy['pct']
        tab_copy[index_list] = tab_copy[index_list].cumsum()
        tab_copy['pct'] = tab_copy['pct'].cumsum()
        tab_copy[index_list] = tab_copy[index_list] / tab_copy['pct']
        tab_copy.sort_values(by='id',ascending=False,inplace=True)
    index_list = define_index(data, counter, target_list, sample_weight)
    cnt_tol = data['cnt'].sum()
    var_x, var_y = var_couple[0], var_couple[1]
    data['bin_x'] = data[var_x].round(3)
    data['bin_y'] = data[var_y].round(3)
    bin_x = list(data['bin_x'].drop_duplicates().sort_values(ascending=ascending))
    bin_y = list(data['bin_y'].drop_duplicates().sort_values(ascending=ascending))
    mesh = pd.merge(pd.DataFrame({'bin_x':bin_x,'flag':1}), pd.DataFrame({'bin_y':bin_y,'flag':1}), how='inner', on='flag')[['bin_x','bin_y']]
    mesh = mesh.merge(data.groupby(by=['bin_x','bin_y'],as_index=False)[index_list].sum(), how='left', on=['bin_x','bin_y']).fillna(0)
    mesh.set_index(['bin_x','bin_y'])
    mesh['id'] = 0
    border = []
    for i in range(tab_copy.shape[0]):
        value = tab_copy.iloc[i]
        id = value['id']
        cnt_req = int(cnt_tol*value['pct'])
        target_min_dict = {}
        for target in target_min_list:
            target_min_dict[target] = value['min_%s' % target]
        target_max_dict = {}
        for target in target_max_list:
            target_max_dict[target] = value['max_%s' % target]
        choice = {}
        for index in index_list:
            choice[index] = 0
        gap_min = np.inf
        while 1:
            if len(border) > 0:
                point_cand = []
                for i,j in enumerate(border):
                    if i == 0 and j < len(bin_y):
                        point_cand.append((i+1,j+1))
                    elif i > 0 and j < border[i-1]:
                        point_cand.append((i+1,j+1))
                else:
                    if i < len(bin_x) - 1:
                        point_cand.append((i+2,1))
            else:
                point_cand = [(1,1)]
            if len(point_cand) == 0:
                break
            cand = mesh.loc[[(bin_x[p[0]-1],bin_y[p[1]-1]) for p in point_cand]].reset_index()
            cand['gap_add'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
            for index in index_list:
                cand[index] += choice[index]
            cand['gap_tol'] = evaluate_gap(cand, target_list, target_min_dict, target_max_dict, target_weight, method)
            if only_gain:
                opt = cand.sort_values(by='gap_add',ascending=True).iloc[0]
            else:
                opt = cand.sort_values(by='gap_tol',ascending=True).iloc[0]
            if min_gain >= 0 and opt['gap_tol'] > gap_min-min_gain:
                break
            point_x = bin_x.index(opt['bin_x']) + 1
            point_y = bin_y.index(opt['bin_y']) + 1
            if point_x <= len(border):
                border[point_x-1] = point_y
            else:
                border.append(point_y)
            for index in index_list:
                choice[index] = opt[index]
            mesh.loc[(opt['bin_x'],opt['bin_y']), 'id'] = id
            if min_gain < 0 and opt['cnt'] >= cnt_req:
                break
    cross_tab = pd.pivot_table(mesh, index='bin_x', columns='bin_y', values='id')
    grouped = mesh.groupby(by='id',as_index=False)[index_list].sum()
    grouped['pct_group'] = grouped['cnt'] / cnt_tol
    for target in target_list:
        grouped['avg_%s' % target] = grouped['sum_%s' % target] / grouped['cnt_%s' % target]
    grouped = tab_conf.merge(grouped[['id','pct_group']+['avg_%s' % target for target in target_list]], how='left', on='id')
    return grouped, cross_tab

def merge_cutting(data, var_list, counter, cnt_req, target_min_dict={}, target_max_dict={}, sample_weight={}, target_weight={}, method='sum', ascending=None, var_min=5, var_max=10, min_gain=0, max_weight=1, step_list=[], n_pro=30):
    def subtask(q_in, q_out, data, var_list, counter, cnt_req, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, var_min, var_max, max_weight):
        while 1:
            try:
                var_weight = q_in.get(timeout=1)
            except:
                continue
            formula = ' + '.join(['%s * %f' % (var_list[i],weight) for i,weight in enumerate(var_weight) if weight > 0])
            data['value'] = data.eval(formula).round(3)
            cutoff = single_cutting(data, 'value', counter, cnt_req, target_min_dict=target_min_dict, target_max_dict=target_max_dict, sample_weight=sample_weight, target_weight=target_weight, method=method, ascending=ascending)
            var_num = len([1 for weight in var_weight if weight > 0])
            gap_add = sum([(weight-max_weight) for weight in var_weight if weight > max_weight])
            cutoff['gap_adj'] = cutoff['gap'] + 10 * gap_add + 100 * (var_min - var_num) * (var_num < var_min) + 100 * (var_num - var_max) * (var_num > var_max)
            cutoff[var_list] = var_weight
            q_out.put(cutoff[['gap_adj']+var_list])
    con = Concurrent(n_pro, subtask, data, var_list, counter, cnt_req, target_min_dict, target_max_dict, sample_weight, target_weight, method, ascending, var_min, var_max, max_weight)
    def calculate(input_list):
        con.put(input_list)
        result = pd.DataFrame()
        for i in tqdm(input_list):
            output = con.get()
            result = result.append(output,ignore_index=True)
        return result
    input_list = [[(1 if i == var else 0) for i in var_list] for var in var_list]
    result_all = calculate(input_list)
    opt = result_all.sort_values(by='gap_adj',ascending=True).iloc[0]
    var_weight_best = list(opt[var_list])
    gap_min = opt['gap_adj']
    for step in step_list:
        while 1:
            var_sub_1 = [var_list[i] for i,weight in enumerate(var_weight_best) if weight > max_weight]
            var_sub_2 = [var_list[i] for i,weight in enumerate(var_weight_best) if weight >= step]
            var_sub = var_sub_1 if len(var_sub_1) > 0 else var_sub_2
            var_add = [var_list[i] for i,weight in enumerate(var_weight_best) if round(weight+step,2) <= max_weight]
            var_weight_cand = []
            for var1 in var_sub:
                for var2 in var_add:
                    if var1 != var2:
                        var_weight = var_weight_best.copy()
                        var_weight[var_list.index(var1)] = round(var_weight[var_list.index(var1)]-step,2)
                        var_weight[var_list.index(var2)] = round(var_weight[var_list.index(var2)]+step,2)
                        var_weight_cand.append(var_weight)
            var_weight_cand = list(pd.concat([result_all.eval('flag=1'), pd.DataFrame(columns=var_list, data=var_weight_cand).eval('flag=0')], axis=0).drop_duplicates(subset=var_list,keep='first').query('flag==0')[var_list])
            var_weight_cand = [list(var_weight) for var_weight in var_weight_cand]
            result = calculate(var_weight_cand)
            result_all = result_all.append(result,ignore_index=True)
            if not result.empty:
                opt = result.sort_values(by='gap_adj',ascending=True).iloc[0]
                if opt['gap_adj'] > gap_min-min_gain:
                    break
                gap_min = opt['gap_adj']
                var_weight_best = list(opt[var_list])
    con.exit()
    var_choice = [var_list[i] for i,weight in enumerate(var_weight_best) if weight > 0]
    var_weight = [weight for weight in var_weight_best if weight > 0]
    return var_choice, var_weight

########################################################################################################################################################################################################

def calc_ks_auc(data, var_list, target_list, weight=None, bins=None, partition=None, ascending=None, n_pro=30):
    def subtask(q_in, q_out, data, index_list, target_list, bins, partition, ascending):
        ascending_list = [ascending] if ascending else [True,False]
        while 1:
            try:
                var = q_in.get(timeout=1)
            except:
                continue
            if bins:
                data['value'] = np.qcut(data.eval(var), bins=bins, duplicates='drop')
            else:
                data['value'] = np.eval(var).round(3)
            columns = ['ks_%s' % target for target in target_list] + ['auc_%s' % target for target in target_list]
            if partition:
                grouped = data.groupby(by=partition+['value'],as_index=False)[index_list].sum()
                result = pd.DataFrame()
                for ascending in ascending_list:
                    temp = grouped.sort_values(by='value',ascending=ascending)
                    temp[['Cum%s' % index for index in index_list]] = temp.groupby(by=partition)[index_list].cumsum()
                    for target in target_list:
                        temp['PctCumBad_%s' % target] = temp['CumBad_%s' % target] / temp['Bad_%s' % target].sum()
                        temp['PctCumGood_%s' % target] = temp['CumGood_%s' % target] / temp['good_%s' % target].sum()
                        temp['ks_%s' % target] = temp['PctCumBad_%s' % target] - temp['PctCumGood_%s' % target]
                        temp['auc_%s' % target] = (temp['PctCumBad_%s' % target] + temp.groupby(by=partition)['PctCumBad_%s' % target].shift(1).fillna(0)) * (temp['PctCumGood_%s' % target] - temp.groupby(by=partition)['PctCumGood_%s' % target].shift(1).fillna(0)) / 2
                    temp = pd.merge(temp.groupby(by=partition,as_index=False)[['ks_%s' % target for target in target_list]].max(), temp.groupby(by=partition,as_index=False)[['auc_%s' % target for target in target_list]].sum(), how='inner', on=partition)
                    result = result.append(temp,ignore_index=True)
                result = result.groupby(by=partition,as_index=False)[columns].max()
            else:
                grouped = data.groupby(by='value',as_index=False)[index_list].sum()
                result = []
                for ascending in ascending_list:
                    temp = grouped.sort_values(by='value',ascending=ascending)
                    temp[['Cum%s' % index for index in index_list]] = temp[index_list].cumsum()
                    for target in target_list:
                        temp['PctCumBad_%s' % target] = temp['CumBad_%s' % target] / temp['Bad_%s' % target].sum()
                        temp['PctCumGood_%s' % target] = temp['CumGood_%s' % target] / temp['good_%s' % target].sum()
                        temp['ks_%s' % target] = temp['PctCumBad_%s' % target] - temp['PctCumGood_%s' % target]
                        temp['auc_%s' % target] = (temp['PctCumBad_%s' % target] + temp['PctCumBad_%s' % target].shift(1).fillna(0)) * (temp['PctCumGood_%s' % target] - temp['PctCumGood_%s' % target].shift(1).fillna(0)) / 2
                    result.append(list(temp[['ks_%s' % target for target in target_list]].max())+list(temp[['auc_%s' % target for target in target_list]].sum()))
                result = pd.DataFrame(columns=columns, data=result)[columns].max()
            result['var'] = var
            q_out.put(result)
    if partition and type(partition) == str:
        partition = [partition]
    index_list = []
    for target in target_list:
        if weight:
            data['Total_%s' % target] = (data[target] >= 0) * data[weight]
            data['Bad_%s' % target] = (data[target] == 1) * data[weight]
            data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        else:
            data['Total_%s' % target] = (data[target] >= 0) * 1
            data['Bad_%s' % target] = (data[target] == 1) * 1
            data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        index_list += ['Bad_%s' % target, 'Good_%s' % target]
    con = Concurrent(n_pro, subtask, data, index_list, target_list, bins, partition, ascending)
    con.put(var_list)
    result = pd.DataFrame()
    for i in tqdm(var_list):
        output = con.get()
        result = result.append(output,ignore_index=True)
    con.exit()
    return result

def iv_binning(data, var_list, target, min_cnt=100, min_pct=0.05, min_iv=0.001, max_bins=10, weight=None, ascending=None, n_pro=30):
    def subtask(q_in, q_out, data, target, min_cnt, min_pct, min_iv, max_bins, ascending):
        while 1:
            try:
                var = q_in.get(timeout=1)
            except:
                continue
            data['value'] = data.eval(var)
            grouped = data.groupby(by='value',as_index=False)[['Total','Bad','Good']].sum()
            grouped['cutoff'] = (grouped['value'] + grouped['value'].shift(-1)) / 2
            intervals = []
            badrates = [grouped['Bad'].sum()/grouped['Total'].sum()]
            index = 0
            while index <= len(intervals):
                lbound = -np.inf if index == 0 else intervals[index-1]
                ubound = np.inf if index == len(intervals) else intervals[index]
                temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].sort_values(by='value',ascending=True)
                temp[['Total_1','Bad_1','Good_1']] = temp[['Total','Bad','Good']].cumsum()
                temp['Total_2'] = temp['Total'].sum() - temp['Total_1']
                temp['Bad_2'] = temp['Bad'].sum() - temp['Bad_1']
                temp['Good_2'] = temp['Good'].sum() - temp['Good_1']
                temp['PctTotal_1'] = temp['Total_1'] / grouped['Total'].sum()
                temp['PctTotal_2'] = temp['Total_2'] / grouped['Total'].sum()
                temp['PctBad_1'] = temp['Bad_1'] / grouped['Bad'].sum()
                temp['PctBad_2'] = temp['Bad_2'] / grouped['Bad'].sum()
                temp['PctGood_1'] = temp['Good_1'] / grouped['Good'].sum()
                temp['PctGood_2'] = temp['Good_2'] / grouped['Good'].sum()
                temp['Badrate_1'] = temp['Bad_1'] / temp['Total_1']
                temp['Badrate_2'] = temp['Bad_2'] / temp['Total_2']
                temp['IV_1'] = (temp['PctBad_1'] - temp['PctGood_1']) * (np.log(temp['PctBad_1']) - np.log(temp['PctGood_1']))
                temp['IV_2'] = (temp['PctBad_2'] - temp['PctGood_2']) * (np.log(temp['PctBad_2']) - np.log(temp['PctGood_2']))
                temp['IV_all'] = (temp['PctBad_1'].max() - temp['PctGood_1'].max()) * (np.log(temp['PctBad_1'].max()) - np.log(temp['PctGood_1'].max()))
                temp['IV_gain'] = temp['IV_1'] + temp['IV_2'] - temp['IV_all']
                temp = temp[(temp['Total_1'] >= min_cnt) & (temp['Total_2'] >= min_cnt)]
                temp = temp[(temp['PctTotal_1'] >= min_pct) & (temp['PctTotal_2'] >= min_pct)]
                temp = temp[(temp['IV_gain'] >= min_iv) & (temp['IV_gain'] < np.inf)]
                if ascending == True:
                    temp = temp[temp['Badrate_1'] <= temp['Badrate_2']]
                    if index > 0:
                        temp = temp[temp['Badrate_1'] >= badrates[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['Badrate_2'] <= badrates[index+1]]
                elif ascending == False:
                    temp = temp[temp['Badrate_1'] >= temp['Badrate_2']]
                    if index > 0:
                        temp = temp[temp['Badrate_1'] <= badrates[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['Badrate_2'] >= badrates[index+1]]
                if not temp.empty:
                    opt = temp.sort_values(by='IV_gain',ascending=False).iloc[0]
                    intervals.insert(index,opt['cutoff'])
                    badrates[index] = opt['Badrate_2']
                    badrates.insert(index,opt['Badrate_1'])
                else:
                    index += 1
            while len(intervals) + 1 > max_bins:
                iv_list = []
                for index, cutoff in enumerate(intervals):
                    lbound = -np.inf if index == 0 else intervals[index-1]
                    ubound = np.inf if index == len(intervals)-1 else intervals[index+1]
                    temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].copy()
                    temp1 = temp[temp['value'] < cutoff].copy()
                    temp2 = temp[temp['value'] > cutoff].copy()
                    values = {}
                    values['PctBad'] = temp['Bad'].sum() / grouped['Bad'].sum()
                    values['PctBad_1'] = temp1['Bad'].sum() / grouped['Bad'].sum()
                    values['PctBad_2'] = temp2['Bad'].sum() / grouped['Bad'].sum()
                    values['PctGood'] = temp['Good'].sum() / grouped['Good'].sum()
                    values['PctGood_1'] = temp1['Good'].sum() / grouped['Good'].sum()
                    values['PctGood_2'] = temp2['Good'].sum() / grouped['Good'].sum()
                    values['IV_all'] = (values['PctBad'] - values['PctGood']) * (np.log(values['PctBad']) - np.log(values['PctGood']))
                    values['IV_1'] = (values['PctBad_1'] - values['PctGood_1']) * (np.log(values['PctBad_1']) - np.log(values['PctGood_1']))
                    values['IV_2'] = (values['PctBad_2'] - values['PctGood_2']) * (np.log(values['PctBad_2']) - np.log(values['PctGood_2']))
                    iv_gain = values['IV_1'] + values['IV_2'] - values['IV_all']
                    iv_list.append(iv_gain)
                index = [i for i,iv in enumerate(iv_list) if iv == min(iv_list)][0]
                _ = intervals.pop(index)
            intervals.insert(0,-np.inf)
            intervals.append(np.inf)
            data['bucket'] = np.cut(data['value'], intervals, include_lowest=True).astype('str')
            result = data.groupby(by='bucket',as_index=False)[['Total','Bad','Good']].sum()
            result['PctTotal'] = result['Total'] / result['Total'].sum()
            result['PctBad'] = result['Bad'] / result['Bad'].sum()
            result['PctGood'] = result['Good'] / result['Good'].sum()
            result['Badrate'] = result['Bad'] / result['Total']
            result['WOE'] = np.log(result['PctBad']) - np.log(result['PctGood'])
            result['IV'] = (result['PctBad'] - result['PctGood']) * result['WOE']
            result['lbound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[0].replace('(','').replace('[','')),3))
            result['ubound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[1].replace(')','').replace(']','')),3))
            result['clus_num'] = result.index + 1
            result['var'] = var
            q_out.put(result)
    if weight:
        data['Total'] = (data[target] >= 0) * data[weight]
        data['Bad'] = (data[target] == 1) * data[weight]
    else:
        data['Total'] = (data[target] >= 0) * 1
        data['Bad'] = (data[target] == 1) * 1
    data['Good'] = data['Total'] - data['Bad']
    con = Concurrent(n_pro, subtask, data, target, min_cnt, min_pct, min_iv, max_bins, ascending)
    con.put(var_list)
    columns = ['var','clus_num','bucket','lbound','ubound','Total','Bad','Good','PctTotal','Badrate','WOE','IV']
    result = pd.DataFrame(columns=columns)
    for i in tqdm(var_list):
        output = con.get()
        result = result.append(output[columns],ignore_index=True)
    con.exit()
    iv_tbl = result.groupby(by='var',as_index=False)['IV'].agg({'bins':'count','IV':'sum'}).sort_values(by='IV',ascending=False)
    bin_tbl = iv_tbl.merge(result, how='inner', on='var', suffixes=('_tol',''))
    bin_tbl['order'] = bin_tbl['bins'] - bin_tbl['clus_num']
    bin_tbl = bin_tbl.sort_values(by=['IV_tol','order'],ascending=False)[columns].reset_index(drop=True)
    return iv_tbl, bin_tbl

def raw2woe(raw_data, var_list, bin_tbl):
    woe_data = raw_data[var_list].copy()
    for var in tqdm(var_list):
        bin_var = bin_tbl[bin_tbl['var'] == var].copy()
        woe_data[var] = 0
        for i in range(bin_var.shape[0]):
            value = bin_var.iloc[i]
            woe_data[var] += (raw_data[var] > value['lbound']) * (raw_data[var] <= value['ubound']) * value['WOE']
    return woe_data

def create_scorecard(lr_res, bin_tbl, score0=660, odds0=1/15, pdo=15, ascending=False):
    B = pdo / np.log(2) * (-1 if ascending == True else 1)
    A = score0 + B * np.log(odds0)
    model_params = lr_res.params
    model_vars = [var for var in model_params.name if var != 'Intercept']
    scorecard = pd.DataFrame()
    for var in model_vars:
        bin_var = bin_tbl[bin_tbl['var'] == var].copy()
        bin_var['score'] = - B * model_params[var] * bin_var['WOE']
        scorecard = scorecard.append(bin_var,ignore_index=True)
    min_score = scorecard.groupby(by='var',as_index=False)['score'].min()
    score_basic = A - B * model_params['Intercept']
    score_amort = (score_basic + min_score.sum()) / min_score.shape[0]
    scorecard = scorecard.merge(min_score, how='inner', on='var')
    scorecard['score_final'] = scorecard.eval('score - min_score + %f' % score_amort).round(0)
    return scorecard

########################################################################################################################################################################################################

import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt

def fwd_select(data, var_list, target, var_initial=[], tol=0.05, var_max=20):
    current_formula = '%s ~ %s + 1' % (target, ' + '.join(var_initial))
    current_score = smf.logit(current_formula, data).fit().aic
    var_choice = var_initial
    var_remain = [var for var in var_list if var not in var_choice]
    while len(var_remain) > 0:
        score_list = []
        for var in var_remain:
            formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice+[var]))
            try:
                res = smf.logit(formula, data).fit(method='newton', maxiter=100, disp=0, tol=tol)
            except Exception as error:
                print('Skipped %s due to %s' % (var, error))
                continue
            score = res.aic 
            converged = res.mle_retvals['converged']
            if converged:
                score_list.append((var,score))
            else: 
                print('Skipped %s due to not converged' % var)
                continue
        score_list.sort(ascending=True)
        best_var, best_score = score_list[0]
        if best_score < current_score:
            var_choice.append(best_var)
            var_remain.remove(best_var)
            current_formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice))
            current_score = best_score
            print('Added %s' % best_var)
            res = smf.logit(current_formula, data).fit(method='newton', maxiter=100, disp=0, tol=tol)
            p_values = res.pvalues
            p_over = p_values[p_values > tol]
            if p_over.shape[0] > 0:
                for name in p_over.index:
                    try:
                        var_choice.remove(name)
                        print('Removed %s due to PValue=%s' % (name, p_over[name]))
                    except ValueError:
                        continue    
        if len(var_choice) >= var_max:
            break
    formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice))
    return formula

def bkwd_select(data, var_list, target, threshold=5):
    var_choice = var_list.copy()
    while 1:
        vif = [variance_inflation_factor(data[var_choice].values,i) for i in range(len(var_choice))]
        if max(vif) > threshold:
            var_drop = [var_choice[i] for i,value in enumerate(vif) if value == max(vif)][0]
            print('Removed %s' % var_drop)
            var_choice.drop(var_drop)
        else:
            break
    formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice))
    return formula

def scorebucket(X, y, lr_res, bins=20):
    model_params = lr_res.params
    ln_odds = (X * model_params).sum(axis=1)
    prob = 1 / (np.exp(-ln_odds)+1)
    prob.name = 'Prob'
    prob = pd.DataFrame(prob)
    prob['Target'] = y 
    prob.sort_values(by='Prob', ascending=False, inplace=True)
    prob['Rank'] = 1
    prob.Rank = prob.Rank.cumsum()
    prob['Bucket'] = pd.qcut(prob.Rank, bins)
    return prob

def ksdistance(prob):   
    bucket = prob.groupby('Bucket',as_index=False)['Target'].agg({'Total':'count','Bad':'sum','BadRate':'mean'})
    bucket.drop('Bucket', axis=1, inplace=True)
    bucket.eval('Good = Total - Bad', inplace=True)
    bucket['CumBad'] = bucket.Bad.cumsum()
    bucket['CumGood'] = bucket.Good.cumsum()
    bucket['CumTotal'] =bucket.Total.cumsum()
    bucket['PctCumBad'] = bucket.CumBad/bucket.CumBad.max()
    bucket['PctCumGood'] = bucket.CumGood/bucket.CumGood.max()
    bucket['PctCumTotal'] = bucket.CumTotal/bucket.CumTotal.max()
    bucket['KS'] = bucket.PctCumBad - bucket.PctCumGood
    bucket.eval('Lift = PctCumBad/PctCumTotal', inplace=True)
    metric_ks = bucket.KS.max()
    bucket[['PctCumBad','PctCumGood','KS']].plot(style=['r','b','g'], xlim=[0,bucket.shape[0]], ylim=[0,1], title='KS Distance = %.4f' % metric_ks)
    plt.xlabel('Score Buckets')
    plt.ylabel('Pct Distribution')
    plt.show() 
    return metric_ks, bucket





