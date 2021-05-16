import pandas as pd
import re


def un_unicode(text):
  patterns = {
    'Nhân vật': '',
    'Series': '',
    'Hãng sản xuất': '',
    'Phát hành': '',
    'Kích thước': '',
    'Tỷ lệ': '',
    'Giá cập nhật tháng': '',
    '[àáảãạăắằẵặẳâầấậẫẩ]': '',
    '[đ]': '',
    '[èéẻẽẹêềếểễệ]': '',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': '',
    '[ùúủũụưừứửữự]': '',
    '[ỳýỷỹỵ]': '',
    '[\t\n\b]': '',
    '[\n]': '',
    '[:]': ''
  }
  output = text
  for regex, replace in patterns.items():
    output = re.sub(regex, replace, str(output))
    # deal with upper case
    output = re.sub(regex.upper(), replace.upper(), output)
  return output

df = pd.read_csv('data/final/data.csv', encoding='utf-8')

df_pub = pd.read_csv('data/final/pubs.csv')

df_pub_single = df_pub.drop_duplicates(subset=['publisher'])
df_pub_single.reset_index(inplace=True)
df_pub_single.drop(['index'], axis=1, inplace=True)
df_pub_single['id'] = df_pub_single.index

# df_pub_single.to_csv('data/final/df_pub_proced.csv', encoding='utf-8', index=False)

for id_item, pub_item in zip(df['id'], df_pub['publisher']):
  for id_pub, pub_name in zip(df_pub_single['id'], df_pub_single['publisher']):
    if pub_item == pub_name:
      df.loc[df['id'] == id_item, 'idPublisher'] = str(int(id_pub))

# df['release_date'] = df['release_date'].apply(lambda x: un_unicode(x))
# df['release_date'] = pd.to_datetime(df['release_date'])
for x in df['release_date']:
  print(x, ' | ', un_unicode(x))

df['price'] = df['price'].apply(lambda x: un_unicode(x))
df['price'] = df['price'].fillna(1000000)

# df['idPublisher'] = pd.to_numeric(df['idPublisher'], downcast='integer')
df.to_csv('data/final/data_proced.csv', encoding='utf-8', index=False)
