class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def hasCycle(head: ListNode) -> bool:
    if head == None:
        return False
    visitats = set()
    cicle = False
    final = False
    visitats.add(head)
    seguent = head.next
    while cicle == False and final == False:
        if seguent in visitats:
            cicle = True
        elif seguent == None:
            final = True
        else:
            visitats.add(seguent)
            seguent = seguent.next
    if final == True:
        return False
    else:
        return True


