# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ShadowsocksPipeline(object):
    def process_item(self, item, spider):

        print("pipline存储数据:"+ spider.name)
        dict_data = dict(item)
        with open('SSR.txt', 'a') as f:
            f.write(str(dict_data['ssURL'][0])+'\n')
        return item
