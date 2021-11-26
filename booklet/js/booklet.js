    $(document).ready(function () {
      $("#booklet").flipBook({
        pages:[
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a111588303754b31c8c3ac_0-front.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a111a015332ceb70150ff2_thumb-0-front.jpeg", title:"Cover"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fb7a464051bf16ffcd_00.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c33d8918f83cc42f3e_thumb-00.jpeg", title:"00"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc3a8061682727daf2_01.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c2f2b1f214d63a49a2_thumb-01.jpeg", title:"01"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fbf3daa210b5894a28_02.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c217f9bfca057f77f4_thumb-02.jpeg", title:"02"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc17f9bf49177e967d_03.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c3206b5a8fdb872c65_thumb-03.jpeg", title:"03"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fb8f37143669b8b787_04.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c35c321f66eb9aed40_thumb-04.jpeg", title:"04"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fbc8291d6fd6079d2e_05.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c3d9507d3f55cd9d4a_thumb-05.jpeg", title:"05"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fbfa8f13dd29d41b9f_06.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c3c8291d4c6e084faf_thumb-06.jpeg", title:"06"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fcd617b909dd945b87_07.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c39cb6fdea105b20a2_thumb-07.jpeg", title:"07"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc7cd2386ef4385481_08.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c375358d5f11c19d99_thumb-08.jpeg", title:"08"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc3704ad60e1b9d3aa_09.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c335113248b445e491_thumb-09.jpeg", title:"09"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc9ff438016fec377a_10.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c317f9bf59a17f77f5_thumb-10.jpeg", title:"10"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc8f3714470db8b788_11.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c3d2986a04cbb2c359_thumb-11.jpeg", title:"11"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc9e838c73d0eff12e_12.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c3ad23e23e92789134_thumb-12.jpeg", title:"12"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fcad23e2b9c577b0f2_13.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c365af7ab4cacaaa39_thumb-13.jpeg", title:"13"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fcd2986a8d63b20177_14.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c3738be16728bdac4e_thumb-14.jpeg", title:"14"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc7a4640663f16ffce_15.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c3dac1d359539283ed_thumb-15.jpeg", title:"15"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc7a4640153516ffda_16.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5d9507da9e7cd9d4b_thumb-16.jpeg", title:"16"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fd8f37148194b8b789_17.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c465af7ab598caaa3a_thumb-17.jpeg", title:"17"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc524b421d51f2f0ee_18.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c4ad23e25685789135_thumb-18.jpeg", title:"18"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc3d8918d3fac35e6d_19.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c307e6e501760eb0fa_thumb-19.jpeg", title:"19"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fd15332c80b512aa35_20.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c47cd238cb40393bbd_thumb-20.jpeg", title:"20"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fd191af4833fb85e80_21.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c4ad4af826682deb49_thumb-21.jpeg", title:"21"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fd2db58b1e5ffddb5e_22.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c4191af442deb8f8f5_thumb-22.jpeg", title:"22"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fc5c8f5938256e0e4f_23.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c4206b5a6101872c6d_thumb-23.jpeg", title:"23"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fd07e6e5209f0e0c79_24.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c47b1c5e2b7cde5fce_thumb-24.jpeg", title:"24"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fd3704ad0d98b9d3c5_25.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c4fa8f139db6d52358_thumb-25.jpeg", title:"25"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fdb01e1570e2593529_26.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c4798ebd78b9c66951_thumb-26.jpeg", title:"26"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fde5c2bc74f4541bbe_27.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c45c8f5960516edb71_thumb-27.jpeg", title:"27"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fdd2986aa4ffb2018a_28.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c4ad4af8dc902deb4a_thumb-28.jpeg", title:"28"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fdbc42b5a66975494f_29.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c4009df34153bc3dac_thumb-29.jpeg", title:"29"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fd07e6e5824f0e0c7a_30.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c42db58b6797feddc7_thumb-30.jpeg", title:"30"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fd07e6e566400e0c7b_31.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5e18d76f848edc049_thumb-31.jpeg", title:"31"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fd5c8f594df16e0e50_32.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5191af48c28b8f913_thumb-32.jpeg", title:"32"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fe42ffc0bba25f2d6a_33.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c57cd2381b27393bbe_thumb-33.jpeg", title:"33"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fe5c8f593af46e0e51_34.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5206b5a9bff872c6e_thumb-34.jpeg", title:"34"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fef3daa246a9894a2d_35.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c55c8f5916256edb72_thumb-35.jpeg", title:"35"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fe9e838cdd0eeff12f_36.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5f951cd1b06c05494_thumb-36.jpeg", title:"36"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fe8bb47a853c44eb56_37.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c42d7ada3b2676e2b6_thumb-37.jpeg", title:"37"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fe17f9bf231f7e96a9_38.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5fc102cfa43794cee_thumb-38.jpeg", title:"38"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fed9507d747dcd0522_39.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5e18d7627a1edc04a_thumb-39.jpeg", title:"39"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6ff9cb6fdd0c45a7921_40.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c68f37148634b990be_thumb-40.jpeg", title:"40"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6fffc102c8a9378835c_41.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5fc102cbfa2794cef_thumb-41.jpeg", title:"41"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6ff65af7ac0bdc9b857_42.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c52db58b2170feddc8_thumb-42.jpeg", title:"42"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6ff65af7ada92c9b859_43.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5743800581bc04dc6_thumb-43.jpeg", title:"43"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6ffd2986a63beb201aa_44.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c54f56292616b31c12_thumb-44.jpeg", title:"44"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6ff199e427d12b74e06_45.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c5ad23e28a25789143_thumb-45.jpeg", title:"45"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6ff009df3375dbb90af_46.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c6dac1d3435992840d_thumb-46.jpeg", title:"46"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6ff65af7ac255c9b863_47.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c6798f2de43436630a_thumb-47.jpeg", title:"47"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d700d9507d86c2cd052c_48.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c6d2986ad9f6b2c35e_thumb-48.jpeg", title:"48"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d6ff5c8f5964546e0e53_49.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c6f3daa2a4828a176d_thumb-49.jpeg", title:"49"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7009e838c33d7eff143_50.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c617f9bf9a387f7822_thumb-50.jpeg", title:"50"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d700798ebd6cddc57431_51.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c6deccc3e71c17c7e1_thumb-51.jpeg", title:"51"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d700798ebd284ec57432_52.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c6798f2d850836630b_thumb-52.jpeg", title:"52"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d700e5c2bc5904541bc4_53.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c64e67731a563be3e7_thumb-53.jpeg", title:"53"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d70075358d37c4c0c6fd_54.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c774252a3b9add8971_thumb-54.jpeg", title:"54"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d700eeb11803badc5f24_55.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c7d2986af4f5b2c361_thumb-55.jpeg", title:"55"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7009e838cb6d3eff144_56.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c75720da5fd1729974_thumb-56.jpeg", title:"56"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7009cb6fd25d65a7932_57.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c74f56293d6ab31c17_thumb-57.jpeg", title:"57"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d700dac1d3ef1291a973_58.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c73a80610c5d28ce19_thumb-58.jpeg", title:"58"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7004e67737a1d3ae497_59.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c7191af4ab72b8f914_thumb-59.jpeg", title:"59"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d70115332c239e12aab2_60.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8dac1d376dd928426_thumb-60.jpeg", title:"60"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7002db58b4f90fddb64_61.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c7ad4af80e402deb4b_thumb-61.jpeg", title:"61"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d70075358d65dec0c6fe_62.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c7524b42864bf36d2a_thumb-62.jpeg", title:"62"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7007a464035d916ffe3_63.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c823015c8b1ba1af7f_thumb-63.jpeg", title:"63"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d700deccc3a7881723f7_64.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c72db58b6122feddc9_thumb-64.jpeg", title:"64"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d700ad4af8128e2d2648_65.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c75c321f70339aed4b_thumb-65.jpeg", title:"65"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7013704ad92d7b9d3f3_66.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c7f2b1f2076f3a49a6_thumb-66.jpeg", title:"66"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d701e47224871be6cfa8_67.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8e5c2bcdb4954b008_thumb-67.jpeg", title:"67"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7018f3714529ab8b7e1_68.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8206b5aacbf872c6f_thumb-68.jpeg", title:"68"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d701b55ad510d9022dab_69.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c7deccc33b7617c7e4_thumb-69.jpeg", title:"69"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7019ff438a2e1ec377d_70.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8524b429098f36d2b_thumb-70.jpeg", title:"70"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d701fa8f1347a2d41bc1_71.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8524b42653cf36d2c_thumb-71.jpeg", title:"71"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7013a80615d5c27daf5_72.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c82d7ada5b2076e2b9_thumb-72.jpeg", title:"72"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d701199e4273f3b74e07_73.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8e18d7628fdedc04d_thumb-73.jpeg", title:"73"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7012d7ada1bc775ef40_74.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8199e42988cb7e1a3_thumb-74.jpeg", title:"74"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d701fc102c7c6b78835d_75.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8191af426f7b8f918_thumb-75.jpeg", title:"75"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d701d617b91338945b8a_76.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8f2b1f274ae3a49a7_thumb-76.jpeg", title:"76"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7019ff4380e7cec377e_77.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c9798ebd1991c66955_thumb-77.jpeg", title:"77"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7017263baed2ab91eb3_78.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c88f371473acb990bf_thumb-78.jpeg", title:"78"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d70107e6e5d67a0e0c7d_79.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c9798ebd673fc66956_thumb-79.jpeg", title:"79"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d7014e6773f3633ae499_80.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c85c8f593f746edb75_thumb-80.jpeg", title:"80"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d70275358d05edc0c6ff_81.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c865af7a3f01caaa3c_thumb-81.jpeg", title:"81"},
          {src:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0d702009df36c4cbb90bc_82-back.jpg", thumb:"https://uploads-ssl.webflow.com/60bf345f64a85ec4d98343c5/61a0f0c8e5c2bc4cbe54b009_thumb-82-back.jpeg", title:"82"}
        ],
        lightBox:true,
        btnPrint:{enabled:false},
        btnDownloadPages:{enabled:false},
        btnDownloadPdf:{enabled:false},
        btnExpand:{enabled:true, hideOnMobile:true}
      });
    })