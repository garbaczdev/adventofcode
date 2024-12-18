package main

import (
	"container/heap"
)

// --- Exported interface ---

type PriorityQueue[T any] struct {
    pqImplementation heapPriorityQueue[T]
}

func (pq *PriorityQueue[T]) Empty() bool {
    return pq.pqImplementation.Len() <= 0
}

func (pq *PriorityQueue[T]) Push(item T, priority int) {
    heap.Push(&pq.pqImplementation, &heapPriorityQueueItem[T]{content: item, priority: priority})
}

func (pq *PriorityQueue[T]) Pop() (T, int) {
    queueItem := heap.Pop(&pq.pqImplementation).(*heapPriorityQueueItem[T])
    return queueItem.content, queueItem.priority
}

func NewPriorityQueue[T any]() PriorityQueue[T] {
    pq := PriorityQueue[T]{
        pqImplementation: heapPriorityQueue[T]{reverseOrder: false},
    }
    heap.Init(&pq.pqImplementation)
    return pq
}

func NewReversePriorityQueue[T any]() PriorityQueue[T] {
    pq := PriorityQueue[T]{
        pqImplementation: heapPriorityQueue[T]{reverseOrder: true},
    }
    heap.Init(&pq.pqImplementation)
    return pq
}


// --- Internal implementation ---

type heapPriorityQueueItem[T any] struct {
    content T
    priority int 
    index int
}

type heapPriorityQueue[T any] struct {
    items []*heapPriorityQueueItem[T]
    reverseOrder bool
}

func (pq heapPriorityQueue[T]) Len() int { return len(pq.items) }

func (pq heapPriorityQueue[T]) Less(i, j int) bool {
    if pq.reverseOrder {
        return pq.items[i].priority < pq.items[j].priority
    } else {
        return pq.items[i].priority > pq.items[j].priority
    }
}

func (pq heapPriorityQueue[T]) Swap(i, j int) {
	pq.items[i], pq.items[j] = pq.items[j], pq.items[i]
	pq.items[i].index = i
	pq.items[j].index = j
}

func (pq *heapPriorityQueue[T]) Push(x any) {
	n := len(pq.items)
	item := x.(*heapPriorityQueueItem[T])
	item.index = n
	pq.items = append(pq.items, item)
}

func (pq *heapPriorityQueue[T]) Pop() any {
	n := len(pq.items)
	item := pq.items[n-1]

	pq.items[n-1] = nil  // don't stop the GC from reclaiming the item eventually
	item.index = -1 // for safety

	pq.items = pq.items[:n-1]
	return item
}
