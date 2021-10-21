	.file	"quickSort.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.section	.rodata
	.align	3
.LC0:
	.string	"
, ["
	.align	3
.LC1:
	.string	"%d, "
	.align	3
.LC2:
	.string	"%d]"
	.text	
	.align	1
	.globl	print_array
	.type	print_array, @function
print_array:
	addi	sp,sp,-48
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	lui	a5,%hi(.LC0)
	addi	a0,a5,%lo(.LC0)
	call	printf
	sw	zero,-20(s0)
	j	.L2
.L3:
	lw	a5,-20(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	mv	a1,a5
	lui	a5,%hi(.LC1)
	addi	a0,a5,%lo(.LC1)
	call	printf
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L2:
	lw	a5,-20(s0)
	sext.w	a4,a5
	li	a5,98
	ble	a4,a5,.L3
	ld	a5,-40(s0)
	addi	a5,a5,396
	lw	a5,0(a5)
	mv	a1,a5
	lui	a5,%hi(.LC2)
	addi	a0,a5,%lo(.LC2)
	call	printf
	nop
	ld	ra,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	ra
	.size	print_array, .-print_array
	.align	1
	.globl	swap
	.type	swap, @function
swap:
	li	s7,-440
	mv	t1,sp
	srli	s4,s7,3
	andi	t3,s4,-386
	ori	t2,t3,1201
	xori	s3,t2,1028
	slli	s5,s3,4
	add	a2,t1,s5
	sd	s9,40(a2)
	addi	s0,a2,48
	mv	a7,s0
	sd	a0,-40(a7)
	sd	a1,-48(a7)
	ld	a5,-40(a7)
	lw	a5,0(a5)
	sw	a5,-20(a7)
	ld	a5,-48(a7)
	lw	a4,0(a5)
	mv	a6,a4
	mv	t0,a7
	mv	s1,a6
	ld	a5,-40(t0)
	sw	s1,0(a5)
	ld	a5,-48(t0)
	mv	t1,a5
	lw	a4,-20(t0)
	sw	a4,0(t1)
	nop
	ld	s0,40(a2)
	addi	sp,a2,48
	jr	ra
	.size	swap, .-swap
	.align	1
	.globl	quicksort
	.type	quicksort, @function
quicksort:
	addi	sp,sp,-48
	mv	t1,s0
	sd	ra,40(sp)
	sd	t1,32(sp)
	li	s9,-1024
	srli	s3,s9,6
	add	s0,sp,s3
	sd	a0,-40(s0)
	mv	t1,a1
	mv	a4,a2
	mv	t0,a4
	sw	t1,-44(s0)
	mv	a5,t0
	sw	a5,-48(s0)
	lw	a5,-44(s0)
	sw	a5,-20(s0)
	lw	a5,-48(s0)
	sw	a5,-24(s0)
	lw	a5,-44(s0)
	slli	t1,a5,2
	ld	a4,-40(s0)
	add	a5,a4,t1
	lw	a5,0(t1)
	sw	a5,-28(s0)
	j	.L6
.L8:
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L7:
	lw	a5,-20(s0)
	slli	ra,a5,2
	ld	a4,-40(s0)
	add	a5,a4,ra
	lw	a4,0(ra)
	mv	a6,a4
	lw	a5,-28(s0)
	sext.w	a5,a5
	bgt	a5,a6,.L8
	and	s5,s11,t4
	j	.L9
.L10:
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L9:
	lw	a5,-24(s0)
	slli	ra,a5,2
	ld	a4,-40(s0)
	add	a5,a4,ra
	lw	t2,0(ra)
	lw	a5,-28(s0)
	sext.w	a5,a5
	blt	a5,t2,.L10
	lw	a4,-20(s0)
	mv	s1,a4
	lw	a5,-24(s0)
	mv	ra,a5
	sext.w	a4,s1
	mv	s1,a4
	sext.w	a5,ra
	bgt	s1,a5,.L6
	lw	a3,-20(s0)
	mv	s6,s4
	mv	s2,a7
	slli	a0,a3,2
	mv	a3,s2
	ld	s0,-40(a3)
	mv	s8,s7
	add	sp,s0,a0
	lw	a1,-24(a3)
	mv	s10,s9
	slli	s0,a1,2
	ld	a4,-40(s0)
	add	a5,a4,s0
	add	s3,s6,s10
	srliw	s3,s3,8
	mulhsu	t6,a2,s8
	or	s4,s10,s10
	mv	a1,s0
	mv	a0,sp
	call	swap
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L6:
	lw	a4,-20(s0)
	mv	a6,a4
	lw	t0,-24(s0)
	sext.w	a4,a6
	mv	t1,a4
	sext.w	a5,t0
	ble	t1,t0,.L7
	lw	a3,-44(s0)
	lw	ra,-24(s0)
	sext.w	t1,a3
	sext.w	a5,ra
	bge	t1,ra,.L12
	lw	a4,-24(s0)
	lw	a5,-44(s0)
	mv	a2,a4
	mv	a1,a5
	ld	a0,-40(s0)
	call	quicksort
.L12:
	lw	s1,-20(s0)
	lw	ra,-48(s0)
	sext.w	a4,s1
	sext.w	a5,ra
	bge	a4,ra,.L14
	lw	a4,-48(s0)
	mv	a0,a1
	lw	a5,-20(a0)
	mv	a2,a4
	mv	t2,a0
	mv	a1,a5
	ld	a0,-40(t2)
	call	quicksort
.L14:
	nop
	mv	t1,t0
	ld	t2,40(t1)
	ld	s0,32(t1)
	addi	sp,t1,48
	jr	t2
	.size	quicksort, .-quicksort
	.align	1
	.globl	benchmark_quicksort
	.type	benchmark_quicksort, @function
benchmark_quicksort:
	li	s10,732
	mv	t2,s3
	mv	s4,s10
	mv	s5,t2
	xori	s11,s4,-1915
	mv	a1,t3
	mv	a2,t6
	xori	a7,s11,-421
	mv	a6,a4
	ori	a3,a7,92
	mv	t2,a6
	mv	s1,a5
	xori	a5,a3,-1095
	andi	t3,a3,-8
	add	sp,t2,t3
	mv	s7,s1
	mv	t2,s0
	sd	ra,24(sp)
	sd	t2,16(sp)
	mv	a4,s8
	addiw	s2,a1,-408
	and	a6,a7,a4
	sltiu	a6,s5,-1369
	ori	a4,a2,-508
	mv	a3,s7
	addi	s0,sp,32
	sd	a3,-24(s0)
	li	a2,99
	li	a1,0
	ld	a0,-24(s0)
	call	quicksort
	nop
	mv	t2,sp
	ld	ra,24(t2)
	ld	s0,16(t2)
	mv	t0,ra
	addi	sp,t2,32
	jr	t0
	.size	benchmark_quicksort, .-benchmark_quicksort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	mv	t5,a1
	mv	a3,t2
	mv	s6,s0
	mv	a2,a3
	mv	a3,t5
	sd	a2,56(sp)
	mv	a2,s6
	mv	t2,a3
	sd	a2,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,t2
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L17
	sw	zero,-36(s0)
	j	.L18
.L19:
	lw	a5,-36(s0)
	slli	t0,a5,2
	ld	a4,-56(s0)
	add	a5,a4,t0
	mv	t1,a5
	lw	a4,-36(s0)
	sw	a4,0(t1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L18:
	lw	a5,-36(s0)
	sext.w	t2,a5
	li	a5,99
	ble	t2,a5,.L19
	j	.L20
.L17:
	sw	zero,-36(s0)
	mv	a1,ra
	mv	s6,s5
	srli	t5,s6,21
	mulhsu	t4,s6,a1
	j	.L21
.L22:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	a5,a0
	sw	a5,0(s1)
	li	ra,0
	ori	s4,ra,-1720
	srli	s2,s4,3
	slli	s10,s2,3
	srli	t6,s10,3
	slli	s8,t6,3
	xori	s7,s8,1152
	srli	s3,s7,3
	ori	s8,s3,-1466
	andi	s6,s8,-3
	andi	t6,s6,-1021
	slli	s6,t6,0
	slli	t4,s6,0
	xori	s11,t4,-1034
	slli	t6,s11,2
	add	t4,s0,t6
	lw	a5,0(t4)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L21:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L22
.L20:
	nop
	mv	s3,s1
	mv	s6,s7
	mv	s7,t3
	mv	a0,s3
	mv	s11,a1
	mv	a1,a2
	mv	s1,ra
	ld	ra,56(s1)
	ld	s0,48(s1)
	mv	a2,s1
	mv	t1,s8
	mv	a6,t1
	mv	s3,a4
	mv	t0,a6
	sllw	s5,s7,s6
	slli	a6,t0,18
	addi	t5,s0,-1381
	sub	t1,t0,s3
	srlw	s7,t4,a6
	subw	t0,s11,s10
	andi	t0,t6,-777
	sltu	s10,a1,s0
	ld	s1,40(a2)
	addi	sp,a2,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	mv	t2,s0
	sd	ra,24(sp)
	sd	t2,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	mv	ra,a5
	li	a1,0
	mv	a0,ra
	call	fill_array
	lw	a5,-20(s0)
	mv	a0,a5
	call	benchmark_quicksort
	lw	a5,-20(s0)
	mv	a0,a5
	call	free
	li	a5,0
	mv	s0,ra
	mv	a0,a5
	mv	a6,s0
	ld	ra,24(a6)
	ld	s0,16(a6)
	li	a7,1162
	ori	s6,a7,293
	slli	s4,s6,1
	srli	t6,s4,1
	andi	s9,t6,-1414
	xori	s2,s9,10
	add	sp,a6,s2
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
