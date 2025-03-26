import random
import time
import copy
from multiprocessing.util import sub_debug


def generate_hole_and_pipe_lengths_sub(total_span,hole_amount,value=True):
    """ Denna funktion har till uppgift att generera, en lista på hur lång respektive
     öppning och pipe ska vara, samt i vilken ordning allting kommer. Allt efter kraven"""
    if value:

        pipe_length_list = []
        hole_length_list = []
        pipe_min_length = 40
        hole_min_length = 85 # ändtra till possible 15 pixels.
        minimum_hole_diff = 20
        minimum_hole_list = []
        for i in range(0, hole_amount):
            minimum_hole_list.append(hole_min_length + i * minimum_hole_diff)
        hole_max_length = 160

        # Först: hur mycket extra får varje  och hål, utöver minimun kraven?
        extra_hole_pixels = []
        for i in range(0, hole_amount):
            extra_hole_pixels.append(0)
        hole_length_differance = []
        for i in range(0, hole_amount - 1):
            hole_length_differance.append(0)
        if len(hole_length_differance) == 0:
            hole_length_differance.append(0)  # iffal jag inte har något hål alls'
        while any(number < minimum_hole_diff for number in hole_length_differance):
            hole_length_list.clear()
            for i in range(0, len(extra_hole_pixels)):
                extra_hole_pixels[i] = random.randrange(0, hole_max_length - minimum_hole_list[i])
            for i in range(0, len(extra_hole_pixels)):
                hole_length_list.append(extra_hole_pixels[i] + minimum_hole_list[i])
            hole_length_list.sort(reverse=True)
            if hole_amount >= 2:
                for i in range(0, hole_amount - 1):
                    hole_length_differance[i] = hole_length_list[i] - hole_length_list[i + 1]
            else:
                break
        # Baserat på hur mycket jag har kvar att alokela. Hur mycket ska varje block få, utöver minimun längd?
        pipe_length_allocate = total_span - sum(hole_length_list) - (hole_amount + 1) * pipe_min_length
        cuts = sorted(random.sample(range(0, pipe_length_allocate), hole_amount))
        cuts.sort(reverse=False)
        if hole_amount==3:
            pipe_length_list.append(cuts[0] + pipe_min_length)
            pipe_length_list.append(cuts[1] - cuts[0] + pipe_min_length)
            pipe_length_list.append(cuts[2] - cuts[1] + pipe_min_length)
            pipe_length_list.append(pipe_length_allocate - cuts[2] + pipe_min_length)
        if hole_amount==2:
            pipe_length_list.append(cuts[0] + pipe_min_length)
            pipe_length_list.append(cuts[1] - cuts[0] + pipe_min_length)
            pipe_length_list.append(pipe_length_allocate - cuts[1] + pipe_min_length)
        if hole_amount == 1:
            pipe_length_list.append(cuts[0] + pipe_min_length)
            pipe_length_list.append(pipe_length_allocate - cuts[0] + pipe_min_length)
        random.shuffle(pipe_length_list)
        random.shuffle(hole_length_list)
    else:
        hole_length_list=[80,random.randint(10,15)]
        pipe_length_list=[100,200, 500-100-200-80-hole_length_list[1]]
        random.shuffle(pipe_length_list)
        random.shuffle(hole_length_list)
    return hole_length_list,pipe_length_list
def generate_hole_and_pipe_lengths(pipe_amount,total_span,hole_amount):
    lista=[]
    for i in range(pipe_amount):
        a,b=generate_hole_and_pipe_lengths_sub(total_span,hole_amount)
        lista.append([a,b])
    return lista

a=generate_hole_and_pipe_lengths(1000,500,1)
print(a)

# def pos_simulation(y_pos,y_vel,frame_amount):
#     """ denna är en simulation som beskriver rangen av var ett objekt kan vara efter x antal frmaes.
#         Med andra ord, vad är superpositionen av alla möjliga y _leds tillstånd?
#         :parameter orginell y posetion, y hastighet samt antal frame som det borde fortgå
#                 obs: Notera att giltiga hastighetr är mellan max hastigheten och inital neg grav
#         :returns En lista med upper lower bound för y värden.
#         """
#
#     # först: definera vilka vilkor jag har, gravitationen, intetiala hopp, tiden innan jag får hoppa igen,
#     time_1=time.time()
#     increment=0.25
#     y_vel_max=5
#     initial_neg_grav=-5
#     edge=2   # vad måste y vel vara innan jag får hoppa igen
#     flap_cooldown= (2-(initial_neg_grav))/increment
#     flap_cooldown_tracker=0
#     if y_vel>=y_vel_max:
#         grav_cooldown=0
#     grav_cooldown=(y_vel_max-y_vel)/increment   # i hur många frmaes får jag accelerera?
#
#
#     # räknar ut lower bound, genom formeln, och genom att att först accelerera och sedan falla konstant
#     if frame_amount < grav_cooldown:
#         y_pos_lower = y_pos + increment * (frame_amount + 1) * frame_amount * (1 / 2) + y_vel * frame_amount
#     else:
#         y_pos_lower=y_pos+increment*(grav_cooldown+1)*grav_cooldown*(1/2)+y_vel*grav_cooldown
#         frame_left=frame_amount-grav_cooldown
#         y_pos_lower += frame_left * y_vel_max
#
#     # räknar nu ut upper bound, genom formeln och genom att kolla hur många gånger jag får hoppa
#     y_vel=initial_neg_grav
#     if frame_amount<flap_cooldown:
#         y_pos_upper=y_pos+increment*(frame_amount+1)*frame_amount*(1/2)+y_vel*frame_amount
#     else:
#         y_pos_upper=0
#         flap_amount=int(frame_amount/flap_cooldown)
#         for i in range(flap_amount):
#             y_pos_upper = y_pos + increment * (flap_cooldown + 1) * flap_cooldown * (1 / 2) + y_vel * flap_cooldown
#             y_pos=y_pos_upper
#         frames_left=frame_amount-(flap_amount)*flap_cooldown
#         y_pos_upper=y_pos + increment * (frames_left + 1) * frames_left * (1 / 2) + y_vel * frames_left
#
#     # nu returnerar jag vad min högsta och lägsta posetion är
#     time_gone=time_1-time.time()
#     return [y_pos_upper,y_pos_lower]

# def ranges_overlap(r1, r2):
#     """ Denna relativa enkla funktiom kollar hur om två ranges överlappr, genom att
#     jämföra start och slut poesitioner för respektive range
#     :parameter mina två ranges, båda i form av en lista med start (lägsta ) posetion först och slutposetion ( högsta) sist
#     :return ett sänning värde (boolean) om mina två ranges överlappar"""
#
#     return r1[0] < r2[1] and r2[0] < r1[1]
# def one_hole_check(start_pos_list,target_pos_list,frame_amount ):
#     """ Denna funktion har till uppgift att kolla om en resväg mellan två hål är möjlig
#         på en viss angiven mängd frames. Meningen är att pipe_check funktionen som är härnästa bygger på den
#     :parameter 2 listor som beskrive rangen poå pipe hålet vi är och ska till. I form av en lista med 2 elemnt, högsta och lägsta värde
#     :returns Ett sanningsvärde om det går eller ej år
#     """
#     hole_pass_value=False
#     y_vel_max=5  # vad är mitt högsta graviation i spelet?
#
#     # räknar ut upperbound och lowerbound genom att ge den så optimala värden som möjligt och checkar sedan med overlap funktionen
#     upper_bound=pos_simulation(start_pos_list[0],0,frame_amount)[0]
#     lower_bound=pos_simulation(start_pos_list[1],0,frame_amount)[1]
#
#     y_pos_range=[upper_bound,lower_bound]
#     y_pos_range_target=[target_pos_list[0],target_pos_list[1]]
#
#
#     return ranges_overlap(y_pos_range,y_pos_range_target)
# def multiple_hole_check(configuration_1,configuration_2,frame_amount):
#     """ denna funktion kollar hur många av mina 9 möjliga resvägar som är gå bara. Kommer därmed returnera en sanningstabbel
#         :parameter mina två pipe configurations, i formen som generate funktionen , samt hur många frames jag får.
#         :returns en lista med 9 sanningsvärden om det går eller ej
#          """
#
#     truth_value=[]
#
#     # här loopar jag igenom och kollar alla pipeconfigurations. Att den är byggd på detta sätt
#     # är för att jag har testat och detta var mönstret jag hittade
#     for i in range(1,4):
#         for j in range(1,4):
#            a=[sum(configuration_1[1][0:i])+sum(configuration_1[0][0:i-1]),
#                                               sum(configuration_1[1][0:i])+sum(configuration_1[0][0:i])]
#            b=[sum(configuration_2[1][0:j])+sum(configuration_2[0][0:j-1]),
#                                               sum(configuration_2[1][0:j]) + sum(configuration_2[0][0:j])]
#
#            truth_value.append(one_hole_check(a,b,frame_amount))
#     return truth_value
# def pipe_list_getter(current_pipe,path_value,pixel_amount,pipe_amount,pipe_list):
#     """ Detta är min masterfunktionen. Den kan ta en pipe som du har nu, samt hela din pipe lista,
#         och med tanke på hur spelet är strukturerad, hur många av resvägarna ska vara möjliga , hur långt bort
#         den ska vara samt hur många du vill välja mellan, returnerar den en lista på olika pipes som fungerar för dig
#         Notera att den bygger på ovannämnda funktioner.
#
#         :parameter nuvarande pipe, hur många av vägarna ska vara möjliga, hur lång bort ska den vara, hur många pipes vill du välja mellan
#                     samt hela din pipe_lista
#         :return en lista med pipes du kan välja mellan. men även tiden det to att käöra hela programmet  """
#
#
#
#     tinme_1=time.time()
#     current_pipe_list=copy.deepcopy(pipe_list) # jag vill ju inte anävnda och modefiera min riktiga pipe_list
#     random.shuffle(current_pipe_list)
#     pipe_answer=[]   # här komemr jag spara mina pipes som fungerar efter kraven och spelets ubbygande
#
#     # här räknar jag ut hur många frmes spelaren får
#     pipe_vel=1.5
#     frame_amount=pixel_amount/pipe_vel
#
#     # här loppar jag igenom alla pipes och kollar om dom fungerar, om dem gör sparar jag det.
#     # loppen körs tills jag inte kan hitta flera elelr jag har hitat mängden jag ville hitta
#     i=0
#     while len(pipe_answer)!=pipe_amount and i<len(current_pipe_list):
#         a=multiple_hole_check(current_pipe,current_pipe_list[i],frame_amount)
#         if a.count(True)==path_value:
#             pipe_answer.append(current_pipe_list[i])
#             print(current_pipe_list[i])
#         i+=1
#     time_2=time.time()
#
#     # returnera svaret
#     return pipe_answer
#
# answer=pipe_list_getter(lista[2],4,10,6,lista)
# print(answer)
# print(len(answer))
# print(lista)
