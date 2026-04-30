# Slice 39K Analytics First Failure Detail Probe

Timestamp: `2026-04-27T07:39:00-04:00`

## Constructor Sanity Output

```text
eval_metric_id=b43bf48e-5bfa-421c-aea5-f182d6890880
model_id=unknown_model
dimension=coherence
metric_name=coherence
score=0.91

```

## Failure Context

```text
285: 2026-04-27 07:39:04,495 - aiosqlite - DEBUG - operation functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>) completed
286: 2026-04-27 07:39:04,495 - aiosqlite - DEBUG - executing functools.partial(<built-in method executemany of sqlite3.Cursor object at 0x7f3802c198c0>, 'INSERT INTO evaluation_metrics (eval_metric_id, inference_id, model_id, dimension, score, reasoning, passed, threshold, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [('395e8613-1127-4977-b82c-70df11c973c8', 'inf_0_coherence', 'unknown_model', 'coherence', 0.77, None, 0, 0.7, '2026-04-26 11:39:04.338048'), ('b4ecadc0-42f5-4522-a5b4-56ebe8e69c7f', 'inf_0_relevance', 'unknown_model', 'relevance', 0.79, None, 0, 0.7, '2026-04-26 11:39:04.338048'), ('9944dc25-8b1a-4d68-9c64-5117eeabe6e3', 'inf_0_factuality', 'unknown_model', 'factuality', 0.78, None, 0, 0.7, '2026-04-26 11:39:04.338048'), ('af780296-9f1c-4330-9277-d87e7a195ab8', 'inf_1_coherence', 'unknown_model', 'coherence', 0.755, None, 0, 0.7, '2026-04-26 12:39:04.338048'), ('8b2664da-1a99-407f-a0e1-a9342ef98ae4', 'inf_1_relevance', 'unknown_model', 'relevance', 0.803, None, 0, 0.7, '2026-04-26 12:39:04.338048'), ('bd1e4fa0-24bf-4d64-a53b-b89689f4a18f', 'inf_1_factuality', 'unknown_model', 'factuality', 0.782, None, 0, 0.7, '2026-04-26 12:39:04.338048'), ('e568ce09-a37b-4ee4-b2bf-fb99904ff8f7', 'inf_2_coherence', 'unknown_model', 'coherence', 0.76, None, 0, 0.7, '2026-04-26 13:39:04.338048'), ('ef985fdf-c663-4348-b293-c256a488d4d9', 'inf_2_relevance', 'unknown_model', 'relevance', 0.806, None, 0, 0.7, '2026-04-26 13:39:04.338048'), ('9972d509-dcca-4d52-ad9f-7d9ba376fecd', 'inf_2_factuality', 'unknown_model', 'factuality', 0.784, None, 0, 0.7, '2026-04-26 13:39:04.338048'), ('2df3c2e0-104f-4d25-ae44-52cd623ad673', 'inf_3_coherence', 'unknown_model', 'coherence', 0.785, None, 0, 0.7, '2026-04-26 14:39:04.338048'), ('4e252e84-d0f4-4cc3-8e7c-d3ae9b023644', 'inf_3_relevance', 'unknown_model', 'relevance', 0.809, None, 0, 0.7, '2026-04-26 14:39:04.338048'), ('f5933682-8cc7-4ebb-bbe9-bdda4049c58a', 'inf_3_factuality', 'unknown_model', 'factuality', 0.786, None, 0, 0.7, '2026-04-26 14:39:04.338048'), ('6b185f8f-1d83-450d-a88a-f637faaaa8cd', 'inf_4_coherence', 'unknown_model', 'coherence', 0.77, None, 0, 0.7, '2026-04-26 15:39:04.338048'), ('815f65c2-fff2-4a09-b2e7-b4efef4a6bfe', 'inf_4_relevance', 'unknown_model', 'relevance', 0.812, None, 0, 0.7, '2026-04-26 15:39:04.338048'), ('1d63de71-9adc-49e8-bd87-f8ff8c0340e7', 'inf_4_factuality', 'unknown_model', 'factuality', 0.788, None, 0, 0.7, '2026-04-26 15:39:04.338048'), ('b9822d55-673f-4c89-8ee8-7c6a85f9a835', 'inf_5_coherence', 'unknown_model', 'coherence', 0.775, None, 0, 0.7, '2026-04-26 16:39:04.338048'), ('5d314714-02c0-441a-85e3-efdc61033603', 'inf_5_relevance', 'unknown_model', 'relevance', 0.805, None, 0, 0.7, '2026-04-26 16:39:04.338048'), ('0a78db63-3c17-4ee1-a9c3-1f55e8e11d58', 'inf_5_factuality', 'unknown_model', 'factuality', 0.79, None, 0, 0.7, '2026-04-26 16:39:04.338048'), ('8d783a96-59d1-405d-870e-6cddd02cab39', 'inf_6_coherence', 'unknown_model', 'coherence', 0.8, None, 0, 0.7, '2026-04-26 17:39:04.338048'), ('6f81cf5f-e4ce-401e-9440-c3dc69af5d55', 'inf_6_relevance', 'unknown_model', 'relevance', 0.8180000000000001, None, 0, 0.7, '2026-04-26 17:39:04.338048'), ('85eeee6c-53e3-4ca7-96d9-197cd178ae67', 'inf_6_factuality', 'unknown_model', 'factuality', 0.792, None, 0, 0.7, '2026-04-26 17:39:04.338048'), ('0636393b-72ac-43eb-b2e6-dfd5089c007e', 'inf_7_coherence', 'unknown_model', 'coherence', 0.785, None, 0, 0.7, '2026-04-26 18:39:04.338048'), ('aada604f-43b1-4c73-89cb-024fed9a1f1b', 'inf_7_relevance', 'unknown_model', 'relevance', 0.8210000000000001, None, 0, 0.7, '2026-04-26 18:39:04.338048'), ('431291dd-2948-4633-a02c-693b6729263e', 'inf_7_factuality', 'unknown_model', 'factuality', 0.794, None, 0, 0.7, '2026-04-26 18:39:04.338048'), ('f3c7a4c4-c4d2-4ee0-8e7c-155340a4caaf', 'inf_8_coherence', 'unknown_model', 'coherence', 0.79, None, 0, 0.7, '2026-04-26 19:39:04.338048'), ('5ced4d94-1294-4add-9b57-a479130395d5', 'inf_8_relevance', 'unknown_model', 'relevance', 0.8240000000000001, None, 0, 0.7, '2026-04-26 19:39:04.338048'), ('b7c519cd-685f-4dd8-add4-302554545a32', 'inf_8_factuality', 'unknown_model', 'factuality', 0.796, None, 0, 0.7, '2026-04-26 19:39:04.338048'), ('9ef88be3-5681-463e-a13b-63fc9d819fe4', 'inf_9_coherence', 'unknown_model', 'coherence', 0.8150000000000001, None, 0, 0.7, '2026-04-26 20:39:04.338048'), ('df4559d5-f552-436d-9664-503a1bd67a27', 'inf_9_relevance', 'unknown_model', 'relevance', 0.8270000000000001, None, 0, 0.7, '2026-04-26 20:39:04.338048'), ('045c293f-4e16-4a80-b8a6-9b46e7c61212', 'inf_9_factuality', 'unknown_model', 'factuality', 0.798, None, 0, 0.7, '2026-04-26 20:39:04.338048'), ('4047b976-b31c-4fec-8c08-77aa7681057a', 'inf_10_coherence', 'unknown_model', 'coherence', 0.8, None, 0, 0.7, '2026-04-26 21:39:04.338048'), ('218af252-71b2-4f21-a3e4-df72744e1e8d', 'inf_10_relevance', 'unknown_model', 'relevance', 0.8200000000000001, None, 0, 0.7, '2026-04-26 21:39:04.338048'), ('060016ee-81bb-4fc6-8c56-cf508eb844fa', 'inf_10_factuality', 'unknown_model', 'factuality', 0.8, None, 0, 0.7, '2026-04-26 21:39:04.338048'), ('ab907566-7037-4fc0-bbcb-e0387c6ae8a2', 'inf_11_coherence', 'unknown_model', 'coherence', 0.805, None, 0, 0.7, '2026-04-26 22:39:04.338048'), ('b29ba43f-05ce-4b38-8bcb-d3a27760fed4', 'inf_11_relevance', 'unknown_model', 'relevance', 0.8330000000000001, None, 0, 0.7, '2026-04-26 22:39:04.338048'), ('86b0db00-7bdf-4cc7-88ed-fb962f2c5f9a', 'inf_11_factuality', 'unknown_model', 'factuality', 0.802, None, 0, 0.7, '2026-04-26 22:39:04.338048'), ('4a222943-39ef-4322-8018-864d8ec3cf64', 'inf_12_coherence', 'unknown_model', 'coherence', 0.8300000000000001, None, 0, 0.7, '2026-04-26 23:39:04.338048'), ('f06d65fa-636b-4b91-b4d8-f34791db43f9', 'inf_12_relevance', 'unknown_model', 'relevance', 0.8360000000000001, None, 0, 0.7, '2026-04-26 23:39:04.338048'), ('ae593f29-e91d-4dd4-9536-9446488002a2', 'inf_12_factuality', 'unknown_model', 'factuality', 0.804, None, 0, 0.7, '2026-04-26 23:39:04.338048'), ('a2b13c76-8aee-469e-afaa-6da2bfe1f26c', 'inf_13_coherence', 'unknown_model', 'coherence', 0.815, None, 0, 0.7, '2026-04-27 00:39:04.338048'), ('e0f4ccc4-cce0-4e7a-89ec-7bcb83d3e245', 'inf_13_relevance', 'unknown_model', 'relevance', 0.8390000000000001, None, 0, 0.7, '2026-04-27 00:39:04.338048'), ('28f31fcc-502a-4bd5-a3be-00b8af44e566', 'inf_13_factuality', 'unknown_model', 'factuality', 0.806, None, 0, 0.7, '2026-04-27 00:39:04.338048'), ('bb265dbe-b9b7-48a3-93d5-7deac5b00fbf', 'inf_14_coherence', 'unknown_model', 'coherence', 0.8200000000000001, None, 0, 0.7, '2026-04-27 01:39:04.338048'), ('dc343690-f8ef-45a3-b662-ddb32bab08e0', 'inf_14_relevance', 'unknown_model', 'relevance', 0.8420000000000001, None, 0, 0.7, '2026-04-27 01:39:04.338048'), ('df15ebfb-fc6a-44c7-b83c-9b83347d2a56', 'inf_14_factuality', 'unknown_model', 'factuality', 0.808, None, 0, 0.7, '2026-04-27 01:39:04.338048'), ('05bd8ec0-6faf-4e82-926e-3449a04fde3c', 'inf_15_coherence', 'unknown_model', 'coherence', 0.845, None, 0, 0.7, '2026-04-27 02:39:04.338048'), ('e7bdc740-8793-4389-9b0d-f294c8c6e376', 'inf_15_relevance', 'unknown_model', 'relevance', 0.8350000000000001, None, 0, 0.7, '2026-04-27 02:39:04.338048'), ('7199b82f-bcdb-4f40-bcb1-d425cd2b2972', 'inf_15_factuality', 'unknown_model', 'factuality', 0.81, None, 0, 0.7, '2026-04-27 02:39:04.338048'), ('ab27d4d4-65c3-46f8-a6fd-0051bc4a5b75', 'inf_16_coherence', 'unknown_model', 'coherence', 0.83, None, 0, 0.7, '2026-04-27 03:39:04.338048'), ('1244d25c-cc31-4a28-89f9-9d48fe591add', 'inf_16_relevance', 'unknown_model', 'relevance', 0.8480000000000001, None, 0, 0.7, '2026-04-27 03:39:04.338048'), ('2f765403-bc43-40d6-a8cd-a622f7c7c389', 'inf_16_factuality', 'unknown_model', 'factuality', 0.812, None, 0, 0.7, '2026-04-27 03:39:04.338048'), ('6a4ea1c0-ecad-41bd-870b-4f28057cfc77', 'inf_17_coherence', 'unknown_model', 'coherence', 0.835, None, 0, 0.7, '2026-04-27 04:39:04.338048'), ('e1595003-7c80-484f-b316-c82b73010ffb', 'inf_17_relevance', 'unknown_model', 'relevance', 0.8510000000000001, None, 0, 0.7, '2026-04-27 04:39:04.338048'), ('331da505-9103-492c-a23f-42a73b306290', 'inf_17_factuality', 'unknown_model', 'factuality', 0.8140000000000001, None, 0, 0.7, '2026-04-27 04:39:04.338048'), ('41dfb6f9-7e4d-4b9b-b687-b1ed6071e71b', 'inf_18_coherence', 'unknown_model', 'coherence', 0.86, None, 0, 0.7, '2026-04-27 05:39:04.338048'), ('3c716d4b-be54-47a5-a592-268e22eaf6f6', 'inf_18_relevance', 'unknown_model', 'relevance', 0.8540000000000001, None, 0, 0.7, '2026-04-27 05:39:04.338048'), ('075a9de8-b0d8-4541-b179-24b439a4787b', 'inf_18_factuality', 'unknown_model', 'factuality', 0.8160000000000001, None, 0, 0.7, '2026-04-27 05:39:04.338048'), ('6e36bb3e-76fa-4751-badb-2a05f310bf52', 'inf_19_coherence', 'unknown_model', 'coherence', 0.845, None, 0, 0.7, '2026-04-27 06:39:04.338048'), ('5c1c5d54-e27a-48a0-92cd-36b85ed49c27', 'inf_19_relevance', 'unknown_model', 'relevance', 0.8570000000000001, None, 0, 0.7, '2026-04-27 06:39:04.338048'), ('3ab2b40e-76ce-4c7c-9a92-1af8c223ad06', 'inf_19_factuality', 'unknown_model', 'factuality', 0.8180000000000001, None, 0, 0.7, '2026-04-27 06:39:04.338048'), ('72166913-58b6-4e2d-a071-3fe91902bfcf', 'inf_20_coherence', 'unknown_model', 'coherence', 0.85, None, 0, 0.7, '2026-04-27 07:39:04.338048'), ('a5ec1da3-492c-43c4-9674-f533cf36ee76', 'inf_20_relevance', 'unknown_model', 'relevance', 0.8500000000000001, None, 0, 0.7, '2026-04-27 07:39:04.338048'), ('b40fe7f7-a1e0-4c19-b7da-8ebf5c565d7a', 'inf_20_factuality', 'unknown_model', 'factuality', 0.8200000000000001, None, 0, 0.7, '2026-04-27 07:39:04.338048'), ('2fbe08d3-006e-4b3f-982a-72cc0e92bf09', 'inf_21_coherence', 'unknown_model', 'coherence', 0.875, None, 0, 0.7, '2026-04-27 08:39:04.338048'), ('96e89020-41a0-425f-a281-6bbda9e75d70', 'inf_21_relevance', 'unknown_model', 'relevance', 0.863, None, 0, 0.7, '2026-04-27 08:39:04.338048'), ('8e49487a-5a40-415a-b00c-9a98a431adab', 'inf_21_factuality', 'unknown_model', 'factuality', 0.8220000000000001, None, 0, 0.7, '2026-04-27 08:39:04.338048'), ('03284139-4e7c-43e2-89c7-1e8fb8e4854f', 'inf_22_coherence', 'unknown_model', 'coherence', 0.86, None, 0, 0.7, '2026-04-27 09:39:04.338048'), ('f2d31533-8a4e-4ca5-88ea-312127ec3086', 'inf_22_relevance', 'unknown_model', 'relevance', 0.8660000000000001, None, 0, 0.7, '2026-04-27 09:39:04.338048'), ('c37cc0cb-96e2-47d8-91a0-c4ba6bf827f1', 'inf_22_factuality', 'unknown_model', 'factuality', 0.8240000000000001, None, 0, 0.7, '2026-04-27 09:39:04.338048'), ('189e70a6-9bda-412e-aa23-32bce579699c', 'inf_23_coherence', 'unknown_model', 'coherence', 0.865, None, 0, 0.7, '2026-04-27 10:39:04.338048'), ('ac4066dd-6299-4ce0-915b-afbd2c8171dd', 'inf_23_relevance', 'unknown_model', 'relevance', 0.869, None, 0, 0.7, '2026-04-27 10:39:04.338048'), ('29869215-69fc-48b5-8947-afdf89667473', 'inf_23_factuality', 'unknown_model', 'factuality', 0.8260000000000001, None, 0, 0.7, '2026-04-27 10:39:04.338048')])
287: 2026-04-27 07:39:04,496 - aiosqlite - DEBUG - operation functools.partial(<built-in method executemany of sqlite3.Cursor object at 0x7f3802c198c0>, 'INSERT INTO evaluation_metrics (eval_metric_id, inference_id, model_id, dimension, score, reasoning, passed, threshold, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [('395e8613-1127-4977-b82c-70df11c973c8', 'inf_0_coherence', 'unknown_model', 'coherence', 0.77, None, 0, 0.7, '2026-04-26 11:39:04.338048'), ('b4ecadc0-42f5-4522-a5b4-56ebe8e69c7f', 'inf_0_relevance', 'unknown_model', 'relevance', 0.79, None, 0, 0.7, '2026-04-26 11:39:04.338048'), ('9944dc25-8b1a-4d68-9c64-5117eeabe6e3', 'inf_0_factuality', 'unknown_model', 'factuality', 0.78, None, 0, 0.7, '2026-04-26 11:39:04.338048'), ('af780296-9f1c-4330-9277-d87e7a195ab8', 'inf_1_coherence', 'unknown_model', 'coherence', 0.755, None, 0, 0.7, '2026-04-26 12:39:04.338048'), ('8b2664da-1a99-407f-a0e1-a9342ef98ae4', 'inf_1_relevance', 'unknown_model', 'relevance', 0.803, None, 0, 0.7, '2026-04-26 12:39:04.338048'), ('bd1e4fa0-24bf-4d64-a53b-b89689f4a18f', 'inf_1_factuality', 'unknown_model', 'factuality', 0.782, None, 0, 0.7, '2026-04-26 12:39:04.338048'), ('e568ce09-a37b-4ee4-b2bf-fb99904ff8f7', 'inf_2_coherence', 'unknown_model', 'coherence', 0.76, None, 0, 0.7, '2026-04-26 13:39:04.338048'), ('ef985fdf-c663-4348-b293-c256a488d4d9', 'inf_2_relevance', 'unknown_model', 'relevance', 0.806, None, 0, 0.7, '2026-04-26 13:39:04.338048'), ('9972d509-dcca-4d52-ad9f-7d9ba376fecd', 'inf_2_factuality', 'unknown_model', 'factuality', 0.784, None, 0, 0.7, '2026-04-26 13:39:04.338048'), ('2df3c2e0-104f-4d25-ae44-52cd623ad673', 'inf_3_coherence', 'unknown_model', 'coherence', 0.785, None, 0, 0.7, '2026-04-26 14:39:04.338048'), ('4e252e84-d0f4-4cc3-8e7c-d3ae9b023644', 'inf_3_relevance', 'unknown_model', 'relevance', 0.809, None, 0, 0.7, '2026-04-26 14:39:04.338048'), ('f5933682-8cc7-4ebb-bbe9-bdda4049c58a', 'inf_3_factuality', 'unknown_model', 'factuality', 0.786, None, 0, 0.7, '2026-04-26 14:39:04.338048'), ('6b185f8f-1d83-450d-a88a-f637faaaa8cd', 'inf_4_coherence', 'unknown_model', 'coherence', 0.77, None, 0, 0.7, '2026-04-26 15:39:04.338048'), ('815f65c2-fff2-4a09-b2e7-b4efef4a6bfe', 'inf_4_relevance', 'unknown_model', 'relevance', 0.812, None, 0, 0.7, '2026-04-26 15:39:04.338048'), ('1d63de71-9adc-49e8-bd87-f8ff8c0340e7', 'inf_4_factuality', 'unknown_model', 'factuality', 0.788, None, 0, 0.7, '2026-04-26 15:39:04.338048'), ('b9822d55-673f-4c89-8ee8-7c6a85f9a835', 'inf_5_coherence', 'unknown_model', 'coherence', 0.775, None, 0, 0.7, '2026-04-26 16:39:04.338048'), ('5d314714-02c0-441a-85e3-efdc61033603', 'inf_5_relevance', 'unknown_model', 'relevance', 0.805, None, 0, 0.7, '2026-04-26 16:39:04.338048'), ('0a78db63-3c17-4ee1-a9c3-1f55e8e11d58', 'inf_5_factuality', 'unknown_model', 'factuality', 0.79, None, 0, 0.7, '2026-04-26 16:39:04.338048'), ('8d783a96-59d1-405d-870e-6cddd02cab39', 'inf_6_coherence', 'unknown_model', 'coherence', 0.8, None, 0, 0.7, '2026-04-26 17:39:04.338048'), ('6f81cf5f-e4ce-401e-9440-c3dc69af5d55', 'inf_6_relevance', 'unknown_model', 'relevance', 0.8180000000000001, None, 0, 0.7, '2026-04-26 17:39:04.338048'), ('85eeee6c-53e3-4ca7-96d9-197cd178ae67', 'inf_6_factuality', 'unknown_model', 'factuality', 0.792, None, 0, 0.7, '2026-04-26 17:39:04.338048'), ('0636393b-72ac-43eb-b2e6-dfd5089c007e', 'inf_7_coherence', 'unknown_model', 'coherence', 0.785, None, 0, 0.7, '2026-04-26 18:39:04.338048'), ('aada604f-43b1-4c73-89cb-024fed9a1f1b', 'inf_7_relevance', 'unknown_model', 'relevance', 0.8210000000000001, None, 0, 0.7, '2026-04-26 18:39:04.338048'), ('431291dd-2948-4633-a02c-693b6729263e', 'inf_7_factuality', 'unknown_model', 'factuality', 0.794, None, 0, 0.7, '2026-04-26 18:39:04.338048'), ('f3c7a4c4-c4d2-4ee0-8e7c-155340a4caaf', 'inf_8_coherence', 'unknown_model', 'coherence', 0.79, None, 0, 0.7, '2026-04-26 19:39:04.338048'), ('5ced4d94-1294-4add-9b57-a479130395d5', 'inf_8_relevance', 'unknown_model', 'relevance', 0.8240000000000001, None, 0, 0.7, '2026-04-26 19:39:04.338048'), ('b7c519cd-685f-4dd8-add4-302554545a32', 'inf_8_factuality', 'unknown_model', 'factuality', 0.796, None, 0, 0.7, '2026-04-26 19:39:04.338048'), ('9ef88be3-5681-463e-a13b-63fc9d819fe4', 'inf_9_coherence', 'unknown_model', 'coherence', 0.8150000000000001, None, 0, 0.7, '2026-04-26 20:39:04.338048'), ('df4559d5-f552-436d-9664-503a1bd67a27', 'inf_9_relevance', 'unknown_model', 'relevance', 0.8270000000000001, None, 0, 0.7, '2026-04-26 20:39:04.338048'), ('045c293f-4e16-4a80-b8a6-9b46e7c61212', 'inf_9_factuality', 'unknown_model', 'factuality', 0.798, None, 0, 0.7, '2026-04-26 20:39:04.338048'), ('4047b976-b31c-4fec-8c08-77aa7681057a', 'inf_10_coherence', 'unknown_model', 'coherence', 0.8, None, 0, 0.7, '2026-04-26 21:39:04.338048'), ('218af252-71b2-4f21-a3e4-df72744e1e8d', 'inf_10_relevance', 'unknown_model', 'relevance', 0.8200000000000001, None, 0, 0.7, '2026-04-26 21:39:04.338048'), ('060016ee-81bb-4fc6-8c56-cf508eb844fa', 'inf_10_factuality', 'unknown_model', 'factuality', 0.8, None, 0, 0.7, '2026-04-26 21:39:04.338048'), ('ab907566-7037-4fc0-bbcb-e0387c6ae8a2', 'inf_11_coherence', 'unknown_model', 'coherence', 0.805, None, 0, 0.7, '2026-04-26 22:39:04.338048'), ('b29ba43f-05ce-4b38-8bcb-d3a27760fed4', 'inf_11_relevance', 'unknown_model', 'relevance', 0.8330000000000001, None, 0, 0.7, '2026-04-26 22:39:04.338048'), ('86b0db00-7bdf-4cc7-88ed-fb962f2c5f9a', 'inf_11_factuality', 'unknown_model', 'factuality', 0.802, None, 0, 0.7, '2026-04-26 22:39:04.338048'), ('4a222943-39ef-4322-8018-864d8ec3cf64', 'inf_12_coherence', 'unknown_model', 'coherence', 0.8300000000000001, None, 0, 0.7, '2026-04-26 23:39:04.338048'), ('f06d65fa-636b-4b91-b4d8-f34791db43f9', 'inf_12_relevance', 'unknown_model', 'relevance', 0.8360000000000001, None, 0, 0.7, '2026-04-26 23:39:04.338048'), ('ae593f29-e91d-4dd4-9536-9446488002a2', 'inf_12_factuality', 'unknown_model', 'factuality', 0.804, None, 0, 0.7, '2026-04-26 23:39:04.338048'), ('a2b13c76-8aee-469e-afaa-6da2bfe1f26c', 'inf_13_coherence', 'unknown_model', 'coherence', 0.815, None, 0, 0.7, '2026-04-27 00:39:04.338048'), ('e0f4ccc4-cce0-4e7a-89ec-7bcb83d3e245', 'inf_13_relevance', 'unknown_model', 'relevance', 0.8390000000000001, None, 0, 0.7, '2026-04-27 00:39:04.338048'), ('28f31fcc-502a-4bd5-a3be-00b8af44e566', 'inf_13_factuality', 'unknown_model', 'factuality', 0.806, None, 0, 0.7, '2026-04-27 00:39:04.338048'), ('bb265dbe-b9b7-48a3-93d5-7deac5b00fbf', 'inf_14_coherence', 'unknown_model', 'coherence', 0.8200000000000001, None, 0, 0.7, '2026-04-27 01:39:04.338048'), ('dc343690-f8ef-45a3-b662-ddb32bab08e0', 'inf_14_relevance', 'unknown_model', 'relevance', 0.8420000000000001, None, 0, 0.7, '2026-04-27 01:39:04.338048'), ('df15ebfb-fc6a-44c7-b83c-9b83347d2a56', 'inf_14_factuality', 'unknown_model', 'factuality', 0.808, None, 0, 0.7, '2026-04-27 01:39:04.338048'), ('05bd8ec0-6faf-4e82-926e-3449a04fde3c', 'inf_15_coherence', 'unknown_model', 'coherence', 0.845, None, 0, 0.7, '2026-04-27 02:39:04.338048'), ('e7bdc740-8793-4389-9b0d-f294c8c6e376', 'inf_15_relevance', 'unknown_model', 'relevance', 0.8350000000000001, None, 0, 0.7, '2026-04-27 02:39:04.338048'), ('7199b82f-bcdb-4f40-bcb1-d425cd2b2972', 'inf_15_factuality', 'unknown_model', 'factuality', 0.81, None, 0, 0.7, '2026-04-27 02:39:04.338048'), ('ab27d4d4-65c3-46f8-a6fd-0051bc4a5b75', 'inf_16_coherence', 'unknown_model', 'coherence', 0.83, None, 0, 0.7, '2026-04-27 03:39:04.338048'), ('1244d25c-cc31-4a28-89f9-9d48fe591add', 'inf_16_relevance', 'unknown_model', 'relevance', 0.8480000000000001, None, 0, 0.7, '2026-04-27 03:39:04.338048'), ('2f765403-bc43-40d6-a8cd-a622f7c7c389', 'inf_16_factuality', 'unknown_model', 'factuality', 0.812, None, 0, 0.7, '2026-04-27 03:39:04.338048'), ('6a4ea1c0-ecad-41bd-870b-4f28057cfc77', 'inf_17_coherence', 'unknown_model', 'coherence', 0.835, None, 0, 0.7, '2026-04-27 04:39:04.338048'), ('e1595003-7c80-484f-b316-c82b73010ffb', 'inf_17_relevance', 'unknown_model', 'relevance', 0.8510000000000001, None, 0, 0.7, '2026-04-27 04:39:04.338048'), ('331da505-9103-492c-a23f-42a73b306290', 'inf_17_factuality', 'unknown_model', 'factuality', 0.8140000000000001, None, 0, 0.7, '2026-04-27 04:39:04.338048'), ('41dfb6f9-7e4d-4b9b-b687-b1ed6071e71b', 'inf_18_coherence', 'unknown_model', 'coherence', 0.86, None, 0, 0.7, '2026-04-27 05:39:04.338048'), ('3c716d4b-be54-47a5-a592-268e22eaf6f6', 'inf_18_relevance', 'unknown_model', 'relevance', 0.8540000000000001, None, 0, 0.7, '2026-04-27 05:39:04.338048'), ('075a9de8-b0d8-4541-b179-24b439a4787b', 'inf_18_factuality', 'unknown_model', 'factuality', 0.8160000000000001, None, 0, 0.7, '2026-04-27 05:39:04.338048'), ('6e36bb3e-76fa-4751-badb-2a05f310bf52', 'inf_19_coherence', 'unknown_model', 'coherence', 0.845, None, 0, 0.7, '2026-04-27 06:39:04.338048'), ('5c1c5d54-e27a-48a0-92cd-36b85ed49c27', 'inf_19_relevance', 'unknown_model', 'relevance', 0.8570000000000001, None, 0, 0.7, '2026-04-27 06:39:04.338048'), ('3ab2b40e-76ce-4c7c-9a92-1af8c223ad06', 'inf_19_factuality', 'unknown_model', 'factuality', 0.8180000000000001, None, 0, 0.7, '2026-04-27 06:39:04.338048'), ('72166913-58b6-4e2d-a071-3fe91902bfcf', 'inf_20_coherence', 'unknown_model', 'coherence', 0.85, None, 0, 0.7, '2026-04-27 07:39:04.338048'), ('a5ec1da3-492c-43c4-9674-f533cf36ee76', 'inf_20_relevance', 'unknown_model', 'relevance', 0.8500000000000001, None, 0, 0.7, '2026-04-27 07:39:04.338048'), ('b40fe7f7-a1e0-4c19-b7da-8ebf5c565d7a', 'inf_20_factuality', 'unknown_model', 'factuality', 0.8200000000000001, None, 0, 0.7, '2026-04-27 07:39:04.338048'), ('2fbe08d3-006e-4b3f-982a-72cc0e92bf09', 'inf_21_coherence', 'unknown_model', 'coherence', 0.875, None, 0, 0.7, '2026-04-27 08:39:04.338048'), ('96e89020-41a0-425f-a281-6bbda9e75d70', 'inf_21_relevance', 'unknown_model', 'relevance', 0.863, None, 0, 0.7, '2026-04-27 08:39:04.338048'), ('8e49487a-5a40-415a-b00c-9a98a431adab', 'inf_21_factuality', 'unknown_model', 'factuality', 0.8220000000000001, None, 0, 0.7, '2026-04-27 08:39:04.338048'), ('03284139-4e7c-43e2-89c7-1e8fb8e4854f', 'inf_22_coherence', 'unknown_model', 'coherence', 0.86, None, 0, 0.7, '2026-04-27 09:39:04.338048'), ('f2d31533-8a4e-4ca5-88ea-312127ec3086', 'inf_22_relevance', 'unknown_model', 'relevance', 0.8660000000000001, None, 0, 0.7, '2026-04-27 09:39:04.338048'), ('c37cc0cb-96e2-47d8-91a0-c4ba6bf827f1', 'inf_22_factuality', 'unknown_model', 'factuality', 0.8240000000000001, None, 0, 0.7, '2026-04-27 09:39:04.338048'), ('189e70a6-9bda-412e-aa23-32bce579699c', 'inf_23_coherence', 'unknown_model', 'coherence', 0.865, None, 0, 0.7, '2026-04-27 10:39:04.338048'), ('ac4066dd-6299-4ce0-915b-afbd2c8171dd', 'inf_23_relevance', 'unknown_model', 'relevance', 0.869, None, 0, 0.7, '2026-04-27 10:39:04.338048'), ('29869215-69fc-48b5-8947-afdf89667473', 'inf_23_factuality', 'unknown_model', 'factuality', 0.8260000000000001, None, 0, 0.7, '2026-04-27 10:39:04.338048')]) completed
288: 2026-04-27 07:39:04,497 - aiosqlite - DEBUG - executing functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f3802c198c0>)
289: 2026-04-27 07:39:04,497 - aiosqlite - DEBUG - operation functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f3802c198c0>) completed
290: 2026-04-27 07:39:04,497 - aiosqlite - DEBUG - executing functools.partial(<built-in method commit of sqlite3.Connection object at 0x7f3802022a70>)
291: 2026-04-27 07:39:04,498 - aiosqlite - DEBUG - operation functools.partial(<built-in method commit of sqlite3.Connection object at 0x7f3802022a70>) completed
292: 2026-04-27 07:39:04,498 - aiosqlite - DEBUG - executing functools.partial(<built-in method rollback of sqlite3.Connection object at 0x7f3802022a70>)
293: 2026-04-27 07:39:04,498 - aiosqlite - DEBUG - operation functools.partial(<built-in method rollback of sqlite3.Connection object at 0x7f3802022a70>) completed
294: 2026-04-27 07:39:04,500 - aiosqlite - DEBUG - executing functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>)
295: 2026-04-27 07:39:04,500 - aiosqlite - DEBUG - operation functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>) completed
296: 2026-04-27 07:39:04,500 - aiosqlite - DEBUG - executing functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f380206b2c0>, 'SELECT evaluation_metrics.eval_metric_id, evaluation_metrics.inference_id, evaluation_metrics.model_id, evaluation_metrics.dimension, evaluation_metrics.score, evaluation_metrics.reasoning, evaluation_metrics.passed, evaluation_metrics.threshold, evaluation_metrics.created_at \nFROM evaluation_metrics \nWHERE evaluation_metrics.dimension = ? AND evaluation_metrics.created_at >= ? ORDER BY evaluation_metrics.created_at DESC', ('coherence', '2026-04-26 11:39:04.498757'))
297: 2026-04-27 07:39:04,500 - aiosqlite - DEBUG - operation functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f380206b2c0>, 'SELECT evaluation_metrics.eval_metric_id, evaluation_metrics.inference_id, evaluation_metrics.model_id, evaluation_metrics.dimension, evaluation_metrics.score, evaluation_metrics.reasoning, evaluation_metrics.passed, evaluation_metrics.threshold, evaluation_metrics.created_at \nFROM evaluation_metrics \nWHERE evaluation_metrics.dimension = ? AND evaluation_metrics.created_at >= ? ORDER BY evaluation_metrics.created_at DESC', ('coherence', '2026-04-26 11:39:04.498757')) completed
298: 2026-04-27 07:39:04,501 - aiosqlite - DEBUG - executing functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f380206b2c0>)
299: 2026-04-27 07:39:04,501 - aiosqlite - DEBUG - operation functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f380206b2c0>) completed
300: 2026-04-27 07:39:04,501 - aiosqlite - DEBUG - executing functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f380206b2c0>)
301: 2026-04-27 07:39:04,501 - aiosqlite - DEBUG - operation functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f380206b2c0>) completed
302: FAILED2026-04-27 07:39:04,659 - aiosqlite - DEBUG - executing functools.partial(<built-in method rollback of sqlite3.Connection object at 0x7f3802022a70>)
303: 2026-04-27 07:39:04,659 - aiosqlite - DEBUG - operation functools.partial(<built-in method rollback of sqlite3.Connection object at 0x7f3802022a70>) completed
304: 2026-04-27 07:39:04,659 - aiosqlite - DEBUG - executing functools.partial(<built-in method rollback of sqlite3.Connection object at 0x7f3802022a70>)
305: 2026-04-27 07:39:04,659 - aiosqlite - DEBUG - operation functools.partial(<built-in method rollback of sqlite3.Connection object at 0x7f3802022a70>) completed
306: 2026-04-27 07:39:04,659 - aiosqlite - DEBUG - executing functools.partial(<built-in method close of sqlite3.Connection object at 0x7f3802022a70>)
307: 2026-04-27 07:39:04,660 - aiosqlite - DEBUG - operation functools.partial(<built-in method close of sqlite3.Connection object at 0x7f3802022a70>) completed
308: 
309: 
310: =================================== FAILURES ===================================
311: ____________________________ test_dimension_trends _____________________________
312: 
313: test_db = <sqlalchemy.orm.session.AsyncSession object at 0x7f38020b7470>
314: sample_evaluation_metrics = None
315: 
316:     @pytest.mark.asyncio
317:     async def test_dimension_trends(test_db: AsyncSession, sample_evaluation_metrics):
318:         """Test dimension trend calculation"""
319:         repo = AnalyticsRepository(test_db)
320:     
321:         trend = await repo.get_dimension_trends("coherence", "literary", hours=24)
322:     
323:         assert isinstance(trend, DimensionTrend)
324:         assert trend.dimension == "coherence"
325: >       assert trend.sample_count == 24
326: E       AssertionError: assert 23 == 24
327: E        +  where 23 = DimensionTrend(dimension='coherence', current_score=0.865, previous_score=0.86, trend=<TrendDirection.STABLE: 'stable'>, change_percent=0.5813953488372098, min_score=0.755, max_score=0.875, avg_score=0.8160869565217391, std_dev=0.035192862194017606, sample_count=23).sample_count
328: 
329: neuroforge_backend/tests/test_analytics_phase_3_0.py:123: AssertionError
330: ------------------------------ Captured log setup ------------------------------
331: DEBUG    asyncio:selector_events.py:64 Using selector: EpollSelector
332: DEBUG    asyncio:selector_events.py:64 Using selector: EpollSelector
333: DEBUG    aiosqlite:core.py:105 executing <function connect.<locals>.connector at 0x7f3802051ee0>
334: DEBUG    aiosqlite:core.py:107 operation <function connect.<locals>.connector at 0x7f3802051ee0> completed
335: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method create_function of sqlite3.Connection object at 0x7f3802022a70>, 'regexp', 2, <function SQLiteDialect_pysqlite.on_connect.<locals>.regexp at 0x7f3802052ca0>, deterministic=True)
336: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method create_function of sqlite3.Connection object at 0x7f3802022a70>, 'regexp', 2, <function SQLiteDialect_pysqlite.on_connect.<locals>.regexp at 0x7f3802052ca0>, deterministic=True) completed
337: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method create_function of sqlite3.Connection object at 0x7f3802022a70>, 'floor', 1, <built-in function floor>, deterministic=True)
338: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method create_function of sqlite3.Connection object at 0x7f3802022a70>, 'floor', 1, <built-in function floor>, deterministic=True) completed
339: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>)
340: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>) completed
341: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f3802043bc0>, 'PRAGMA read_uncommitted', [])
342: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f3802043bc0>, 'PRAGMA read_uncommitted', []) completed
343: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f3802043bc0>)
344: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f3802043bc0>) completed
345: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f3802043bc0>)
346: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f3802043bc0>) completed
347: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method rollback of sqlite3.Connection object at 0x7f3802022a70>)
348: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method rollback of sqlite3.Connection object at 0x7f3802022a70>) completed
349: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>)
350: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>) completed
351: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f38020696c0>, 'PRAGMA main.table_info("inferences")', ())
352: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f38020696c0>, 'PRAGMA main.table_info("inferences")', ()) completed
353: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f38020696c0>)
354: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f38020696c0>) completed
355: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f38020696c0>)
356: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f38020696c0>) completed
357: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>)
358: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>) completed
359: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f380206b4c0>, 'PRAGMA temp.table_info("inferences")', ())
360: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f380206b4c0>, 'PRAGMA temp.table_info("inferences")', ()) completed
361: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f380206b4c0>)
362: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f380206b4c0>) completed
363: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f380206b4c0>)
364: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method close of sqlite3.Cursor object at 0x7f380206b4c0>) completed
365: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>)
366: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method cursor of sqlite3.Connection object at 0x7f3802022a70>) completed
367: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f380206b5c0>, 'PRAGMA main.table_info("model_metrics")', ())
368: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method execute of sqlite3.Cursor object at 0x7f380206b5c0>, 'PRAGMA main.table_info("model_metrics")', ()) completed
369: DEBUG    aiosqlite:core.py:105 executing functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f380206b5c0>)
370: DEBUG    aiosqlite:core.py:107 operation functools.partial(<built-in method fetchall of sqlite3.Cursor object at 0x7f380206b5c0>) completed
```

## Test Source Context: test_dimension_trends

```python
95:             inference_id=f"test_inf_{i}",
96:             domain="literary",
97:             task_type="analysis",
98:             model_id="test_model_1",
99:             context_pack_id=f"pack_{i}",
100:             output=f"Test output {i}",
101:             status="completed" if i % 5 != 0 else "failed",
102:             correlation_id=f"corr_{i}",
103:             created_at=base_time + timedelta(hours=i)
104:         )
105:         test_db.add(inference)
106: 
107:     await test_db.commit()
108: 
109: 
110: # ============================================================================
111: # Analytics Repository Tests
112: # ============================================================================
113: 
114: @pytest.mark.asyncio
115: async def test_dimension_trends(test_db: AsyncSession, sample_evaluation_metrics):
116:     """Test dimension trend calculation"""
117:     repo = AnalyticsRepository(test_db)
118: 
119:     trend = await repo.get_dimension_trends("coherence", "literary", hours=24)
120: 
121:     assert isinstance(trend, DimensionTrend)
122:     assert trend.dimension == "coherence"
123:     assert trend.sample_count == 24
124:     assert trend.avg_score > 0.7
125:     assert trend.min_score <= trend.avg_score <= trend.max_score
126:     assert trend.std_dev >= 0
127: 
128: 
129: @pytest.mark.asyncio
130: async def test_model_stats(test_db: AsyncSession, sample_inferences, sample_evaluation_metrics):
131:     """Test model performance statistics"""
132:     repo = AnalyticsRepository(test_db)
133: 
134:     stats = await repo.get_model_stats("test_model_1", "literary", hours=24)
135: 
136:     assert isinstance(stats, PerformanceStats)
137:     assert stats.model_id == "test_model_1"
138:     assert stats.domain == "literary"
139:     assert stats.total_inferences == 20
140:     assert 0.0 <= stats.success_rate <= 1.0
141:     assert 0.0 <= stats.overall_score <= 1.0
142: 
143: 
144: @pytest.mark.asyncio
145: async def test_comparative_analysis(test_db: AsyncSession, sample_inferences, sample_evaluation_metrics):
146:     """Test multi-model comparison"""
147:     repo = AnalyticsRepository(test_db)
148: 
149:     # Create inferences for multiple models
150:     for model_id in ["model_2", "model_3"]:
151:         for i in range(10):
152:             inf = Inference(
153:                 inference_id=f"inf_{model_id}_{i}",
154:                 domain="literary",
155:                 task_type="analysis",
156:                 model_id=model_id,
157:                 context_pack_id=f"pack_{i}",
158:                 output=f"Output from {model_id}",
159:                 status="completed",
160:                 created_at=datetime.now(UTC).replace(tzinfo=None) - timedelta(hours=24 - i)
161:             )
162:             test_db.add(inf)
163: 
164:     await test_db.commit()
165: 
166:     comparison = await repo.get_comparative_analysis(
167:         ["test_model_1", "model_2", "model_3"],
168:         "literary",
169:         hours=24
170:     )
171: 
172:     assert comparison["domain"] == "literary"
173:     assert "models" in comparison
174:     assert "top_model" in comparison
175: 
176: 
177: @pytest.mark.asyncio
178: async def test_anomaly_detection_basic(test_db: AsyncSession, sample_evaluation_metrics):
179:     """Test basic anomaly detection with z-score"""
180:     repo = AnalyticsRepository(test_db)
181: 
182:     # Add anomaly (very high score)
183:     anomaly_metric = EvaluationMetric(
184:         metric_name="coherence",
185:         score=1.0,  # Unusually high
186:         inference_id="anomaly_inf",
187:         created_at=datetime.now(UTC).replace(tzinfo=None)
188:     )
189:     test_db.add(anomaly_metric)
190:     await test_db.commit()
191: 
192:     alerts = await repo.detect_anomalies("test_model_1", "literary", window_hours=1)
193: 
194:     # Should detect anomaly (z > 2)
195:     assert len(alerts) > 0
196:     assert any(a.severity in ["high", "critical"] for a in alerts)
197: 
198: 
199: @pytest.mark.asyncio
200: async def test_predict_champion_transition(test_db: AsyncSession, sample_inferences):
201:     """Test champion transition prediction"""
202:     repo = AnalyticsRepository(test_db)
203: 
204:     prediction = await repo.predict_next_champion("literary", hours=24)
205: 
206:     assert isinstance(prediction, dict)
207:     assert "model_id" in prediction
208:     assert 0.0 <= prediction["next_champion_prob"] <= 1.0
209:     assert isinstance(prediction["factors"], list)
210: 
211: 
212: # ============================================================================
213: # Performance Predictor Tests
214: # ============================================================================
215: 
216: @pytest.mark.asyncio
217: async def test_performance_trajectory(test_db: AsyncSession, sample_evaluation_metrics):
218:     """Test performance trajectory prediction"""
219:     predictor = PerformancePredictor(test_db)
220: 
221:     trajectory = await predictor.predict_performance_trajectory(
222:         "test_model_1",
223:         "literary",
224:         hours_ahead=6
225:     )
226: 
227:     assert isinstance(trajectory, PerformanceTrajectory)
228:     assert trajectory.model_id == "test_model_1"
229:     assert trajectory.current_score > 0
230:     assert trajectory.predicted_score > 0
231:     assert 0.5 <= trajectory.confidence <= 1.0
232:     assert len(trajectory.milestones) > 0
233: 
234: 
235: @pytest.mark.asyncio
```

## Model Source Context: EvaluationMetric

```python
137:     previous_champion_id = Column(String(256), nullable=True)
138:     previous_champion_provider = Column(String(50), nullable=True)
139:     reason_for_rotation = Column(String(500), nullable=True)
140:     
141:     # Metadata
142:     rotation_count = Column(Integer, default=1)
143:     created_at = Column(DateTime, default=datetime.utcnow)
144:     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
145: 
146: 
147: class EvaluationMetric(Base):
148:     """Persistent evaluation dimension scores for trend analysis"""
149:     __tablename__ = "evaluation_metrics"
150:     
151:     # Primary key
152:     eval_metric_id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid4()))
153:     # Association
154:     inference_id = Column(String(36), ForeignKey("inferences.inference_id"), index=True, nullable=False)
155:     model_id = Column(String(256), index=True, nullable=False, default="unknown_model")
156:     # Evaluation dimension
157:     dimension = Column(String(50), nullable=False)  # coherence, relevance, factuality, etc.
158:     # Compatibility alias for analytics constructor contract.
159:     metric_name = synonym("dimension")
160:     score = Column(Float, nullable=False)  # 0.0 to 1.0
161:     reasoning = Column(String(1000), nullable=True)
162:     passed = Column(Boolean, default=False)
163:     threshold = Column(Float, default=0.7)
164:     
165:     # Tracking
166:     created_at = Column(DateTime, default=datetime.utcnow, index=True)
167:     
168:     # Indexes for trend analysis
169:     __table_args__ = (
170:         Index("idx_model_dimension_created", "model_id", "dimension", "created_at"),
171:         Index("idx_inference_dimension", "inference_id", "dimension"),
172:     )
173: 
174:     def __init__(self, **kwargs):
175:         # Compatibility guard for legacy analytics fixture/runtime construction.
176:         if "metric_name" in kwargs and "dimension" not in kwargs:
177:             kwargs["dimension"] = kwargs.pop("metric_name")
178:         else:
179:             kwargs.pop("metric_name", None)
180:     
181:         if not kwargs.get("eval_metric_id"):
182:             kwargs["eval_metric_id"] = str(uuid4())
183:         if kwargs.get("model_id") is None:
184:             kwargs["model_id"] = "unknown_model"
185:     
186:         valid_keys = {prop.key for prop in self.__mapper__.attrs}
187:         for key, value in kwargs.items():
188:             if key not in valid_keys:
189:                 raise TypeError(f"{key!r} is an invalid keyword argument for {self.__class__.__name__}")
190:             setattr(self, key, value)
191: 
```
