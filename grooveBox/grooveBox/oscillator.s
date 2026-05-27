.text
.global next_sample
.type next_sample, %function

// int32_t next_sample(uint32_t *phase, uint32_t increment, uint32_t amp)
// x0 = pointer to phase
// w1 = increment
// w2 = amp 0-1024
// return w0 = signed sample

next_sample:
    ldr w2, [x0]
    add w2, w2, w1
    str w2, [x0]

    lsr w0, w2, #16

    movz w3, #0x8000
    sub w0, w0, w3

    ret