listx = [["0.022891","36883.9758"],["0.022878","27.0693"],["0.022851","8.6821"],["0.022844","6.2567"],["0.022843","8.3536"],["0.02284","59.9927"],["0.022831","22.5628"],["0.022823","110.1394"],["0.02282","96.9079"],["0.022816","7.5228"],["0.022814","122.0533"],["0.022806","7.9131"],["0.022804","7.4984"],["0.0228","121.0031"],["0.022796","24.5552"],["0.022791","12.1618"],["0.02278","45.801"],["0.022777","2492.9193"],["0.022776","1738.299"],["0.02277","33.8898"],["0.022768","25.5163"],["0.022764","27.0693"],["0.022763","21.5482"],["0.022735","8.5155"],["0.022729","8.3914"],["0.022723","8.6821"],["0.022716","6.5984"],["0.022713","139.8513"],["0.022708","788.6562"],["0.0227","9.3837"],["0.022699","202.3715"],["0.022697","8.3536"],["0.022696","294.3007"],["0.022692","18.1571"],["0.022691","129.6016"],["0.02269","219.178"],["0.022681","24.5552"],["0.022678","574.4778"],["0.022677","14.1698"],["0.022676","326.0258"],["0.022668","122.0533"],["0.022667","71.4116"],["0.022656","21.4494"],["0.022655","7.4984"],["0.022654","132.7022"],["0.02265","52.5656"],["0.02264","116.2886"],["0.022636","1688.2318"],["0.022624","44.5525"],["0.022621","25.5163"],["0.02262","1494.732"],["0.02261","5.6808"],["0.022607","2852.8745"],["0.0226","121.0031"],["0.022595","8.6821"],["0.022586","21.5482"],["0.022584","45.801"],["0.022577","905.5823"],["0.022572","8.3914"],["0.02257","212.2963"],["0.022566","24.5552"],["0.02256","155.8447"],["0.022551","8.3536"],["0.022548","7.9131"],["0.022543","202.3715"],["0.02254","59.9927"],["0.022539","1403.3254"],["0.022536","27.0693"],["0.022525","30.0012"],["0.022523","518.2836"],["0.022522","122.0533"],["0.02252","139.8513"],["0.022514","71.4116"],["0.02251","12.1025"],["0.022509","1334.3449"],["0.022506","7.4984"],["0.022498","56.6396"],["0.022491","3181.406"],["0.02249","18.1571"],["0.022488","162.9301"],["0.022486","129.6016"],["0.022485","110.1394"],["0.02248","25.4963"],["0.022477","22.5628"],["0.022474","25.5163"],["0.022467","8.6821"],["0.022453","6457.9342"],["0.022452","788.6562"],["0.022451","24.5552"],["0.02245","1261.9521"],["0.022449","73.1459"],["0.022446","294.3007"],["0.022437","311417.3044"],["0.022436","10082.1345"],["0.022432","7.5228"],["0.022431","812.339"],["0.022422","27.0693"],["0.022421","27042.8667"],["0.02242","178.6353"],["0.022419","7.9131"]]
sum = 0
sum2 = 0

for i in range(len(listx)):
    sum += float(listx[i][1])
    sum2 += float(listx[i][0]) * float(listx[i][1])
    if sum > 255216:
        sum2 = sum2 / sum
        break

print(sum2)