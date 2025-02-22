from django.template import Library
 
register = Library()
 
@register.filter
def paginatebyfive(lis):
	lists = []
	for i in range(1,-(-len(lis)//5)+1):
		minilist = []
		for j in lis[(i-1)*5:i*5]:
			minilist.append(j)
		lists.append(minilist)
	return lists
