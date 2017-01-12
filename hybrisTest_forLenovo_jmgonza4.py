#!/usr/bin/python
'''
This code extracts metadata of interest and stores it in a csv file
'''
import pyexcel as pe
from lxml import html
import requests
import string

# webpage of interest
url="http://shop.lenovo.com/us/en/tablets/lenovo/yoga-book/yoga-book-android/?menu-id=yoga_book_android"
# name of output csv file (no extension!)
csv_filename="test"


# metadata of interest
meta_names=["InternalSearchCanonical","ProductName","InternalSearchCanonical","ProductName","Title",\
        "Area","ModelNumber","THUMBNAIL_URL","ModelNameVariants","SKU","Description","metaprocessor",\
        "metaoperatingsystem","metatotalmemory","metasystemgraphics","metadisplaytype","metaharddrive",\
        "metabattery","metanetworkinterfacetype","metabluetooth","metawarranty","metawarranty_details",\
        "metaram","metaidentifier"]


# get html info 
def get_html(url): 
    page=requests.get(url)
    tree=html.fromstring(page.text)
    headers=tree.xpath('//*[@id="tab-customize"]/div[2]/div[2]/ol/li[1]/div[3]/div/div[1]')
    return tree,headers


# get metadata info
def get_meta(tree,metaList):
    meta_attr={}
    for meta in metaList:
        lst=tree.xpath('//meta[@name="'+meta+'"]')
        if len(lst) != 0:
            for i in lst:
                meta_attr[meta]=i.attrib["content"]
        else:
            meta_attr[meta]=""
    return meta_attr 


# change name of keys and sort for csv file
def rename_sort_keys(metaDict):
    meta=["" for key in xrange(len(metaDict.keys()))]
    attr=["" for key in xrange(len(metaDict.keys()))]
    for key in metaDict:
        if key == "InternalSearchCanonical":
            meta[0]="Site Address"
            attr[0]=metaDict[key]
        if key == "ProductName":
            meta[1]="Product Group"
            attr[1]=metaDict[key]
        if key == "Title":
            meta[2]="Title"
            attr[2]=metaDict[key]
        if key == "Area":
            meta[3]="Area"
            attr[3]=metaDict[key]
        if key == "ModelNumber":
            meta[4]="Product Name"
            attr[4]=metaDict[key]
        if key == "THUMBNAIL_URL":
            meta[5]="Thumbnail URL"
            attr[5]=metaDict[key]
        if key == "ModelNameVariants":
            meta[6]="Alt Product Name"
            attr[6]=metaDict[key]
        if key == "SKU":
            meta[7]="SKU"
            attr[7]=metaDict[key]
        if key == "Description":
            meta[8]="Description"
            attr[8]=metaDict[key]
        if key == "metaprocessor":
            meta[9]="Processor"
            attr[9]=metaDict[key]
        if key == "metaoperatingsystem":
            meta[10]="OS"
            attr[10]=metaDict[key]
        if key == "metatotalmemory":
            meta[11]="Total Mem"
            attr[11]=metaDict[key]
        if key == "metasystemgraphics":
            meta[12]="Graphics"
            attr[12]=metaDict[key]
        if key == "metadisplaytype":
            meta[13]="Display"
            attr[13]=metaDict[key]
        if key == "metaharddrive":
            meta[14]="Hard Drive"
            attr[14]=metaDict[key]
        if key == "metabattery":
            meta[15]="Battery"
            attr[15]=metaDict[key]
        if key == "metanetworkinterfacetype":
            meta[16]="Network Card"
            attr[16]=metaDict[key]
        if key == "metabluetooth":
            meta[17]="Bluetooth"
            attr[17]=metaDict[key]
        if key == "metawarranty":
            meta[18]="Warranty"
            attr[18]=metaDict[key]
        if key == "metawarranty_details":
            meta[19]="Warranty Details"
            attr[19]=metaDict[key]
        if key == "metaram":
            meta[20]="RAM"
            attr[20]=metaDict[key]
        if key == "metaidentifier":
            meta[21]="OIDs on page"
            attr[21]=metaDict[key]
    return meta,attr


# make csv file
def make_csv(meta,attr,csv_name):
    data=[meta,attr] 
    pe.save_as(array=data,dest_file_name=csv_name+".csv",dest_delimiter=",")



# run program
def main():
    print "Extracting metadata from:\n",url
    html=get_html(url)
    print "...sorting data..."
    meta_data_sorted=rename_sort_keys(get_meta(html[0],meta_names))
    make_csv(meta_data_sorted[0],meta_data_sorted[1],csv_filename)
    print "Done.\nData located in: "+csv_filename+".csv"

main()

