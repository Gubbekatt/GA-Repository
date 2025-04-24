import random


def generate_hole_and_pipe_lengths_sub(total_span,hole_amount,value=True):
    """ 
    Denna funktion har till uppgift att generera, en lista på hur lång respektive
     öppning och pipe ska vara, samt i vilken ordning allting kommer. Allt efter kraven;
     Huvud-ideen, är att man bestämmer hur mycket varje del av pipen får extra, utöver minmun-kraven
     """
    
    if value:
        # Här följer alla kraven för pipe-uppsättningen
        pipe_length_list = []
        hole_length_list = []
        pipe_min_length = 40
        hole_min_length = 85 # ändtra till possible 15 pixels.
        minimum_hole_diff = 20
        
        minimum_hole_list = []
        for i in range(0, hole_amount):
            minimum_hole_list.append(hole_min_length + i * minimum_hole_diff)
        hole_max_length = 160

        # Räknar ut hur långt varje hål ska vara
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
                
        # Med hål-längderna satta, hur långt skall varje block vara?
        
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
        # Sätter ett manuelt värde, används i version 2
        hole_length_list=[80,random.randint(10,15)]
        pipe_length_list=[100,200, 500-100-200-80-hole_length_list[1]]
        random.shuffle(pipe_length_list)
        random.shuffle(hole_length_list)
    return hole_length_list,pipe_length_list
    
def generate_hole_and_pipe_lengths(pipe_amount,total_span,hole_amount):
    """
    Utefrån ovan funktion genereras dem faktiska pipe uppsättningarna, total 1000 av dem
    """
    lista=[]
    for i in range(pipe_amount):
        a,b=generate_hole_and_pipe_lengths_sub(total_span,hole_amount)
        lista.append([a,b])
    return lista

a=generate_hole_and_pipe_lengths(1000,500,1)
print(a)

