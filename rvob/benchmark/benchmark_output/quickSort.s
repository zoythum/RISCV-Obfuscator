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
	addi	sp,sp,-48
	sd	s0,40(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	ra,s0
	sd	a1,-48(ra)
	ld	a5,-40(ra)
	lw	a5,0(a5)
	sw	a5,-20(ra)
	ld	a5,-48(ra)
	lw	a4,0(a5)
	ld	a5,-40(ra)
	sw	a4,0(a5)
	ld	a5,-48(ra)
	lw	a4,-20(ra)
	sw	a4,0(a5)
	nop
	ld	s0,40(sp)
	addi	sp,sp,48
	jr	ra
	.size	swap, .-swap
	.align	1
	.globl	quicksort
	.type	quicksort, @function
quicksort:
	addi	sp,sp,-48
	mv	a4,s0
	sd	ra,40(sp)
	sd	a4,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	mv	ra,a5
	mv	a4,a2
	sw	ra,-44(s0)
	mv	a5,a4
	sw	a5,-48(s0)
	lw	a5,-44(s0)
	sw	a5,-20(s0)
	lw	a5,-48(s0)
	sw	a5,-24(s0)
	lw	a5,-44(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a5,0(a5)
	sw	a5,-28(s0)
	j	.L6
.L8:
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L7:
	lw	a5,-20(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a4,0(a5)
	lw	a5,-28(s0)
	sext.w	a5,a5
	bgt	a5,a4,.L8
	j	.L9
	srl	t1,s3,s8
	mulw	s4,s3,s4
	addiw	ra,s3,405
.L10:
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L9:
	lw	a5,-24(s0)
	slli	a5,a5,2
	mv	ra,a5
	ld	a4,-40(s0)
	add	a5,a4,ra
	lw	a4,0(a5)
	lw	a5,-28(s0)
	sext.w	a5,a5
	blt	a5,a4,.L10
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	and	s9,t3,s7
	sll	s2,s6,s11
	mv	s4,s10
	slt	a7,ra,ra
	addw	t2,s11,t6
	mv	sp,a5
	sll	s4,s10,t2
	sext.w	a4,a4
	sext.w	a5,sp
	bgt	a4,a5,.L6
	subw	s2,t1,s6
	addiw	ra,t5,-483
	xor	a1,s7,t1
	lw	a5,-20(s0)
	slli	a5,a5,2
	mv	sp,a5
	ld	a4,-40(s0)
	add	a3,a4,sp
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	mv	a1,a5
	mv	a0,a3
	call	swap
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L6:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	sext.w	a4,a4
	sext.w	a5,a5
	ble	a4,a5,.L7
	lw	a4,-44(s0)
	lw	a5,-24(s0)
	sll	s11,s2,s2
	slt	s10,s2,s9
	slt	t5,s7,a3
	sext.w	a4,a4
	sext.w	a5,a5
	bge	a4,a5,.L12
	lw	a4,-24(s0)
	lw	a5,-44(s0)
	mv	a2,a4
	mv	a1,a5
	ld	a0,-40(s0)
	call	quicksort
.L12:
	lw	a4,-20(s0)
	lw	a5,-48(s0)
	sext.w	a4,a4
	sext.w	a5,a5
	bge	a4,a5,.L14
	lw	a4,-48(s0)
	lw	a5,-20(s0)
	mv	a2,a4
	mv	a1,a5
	ld	a0,-40(s0)
	sll	a3,a7,a7
	slliw	s10,s1,25
	or	s5,t0,t2
	call	quicksort
.L14:
	nop
	ld	t0,40(sp)
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	t0
	.size	quicksort, .-quicksort
	.align	1
	.globl	benchmark_quicksort
	.type	benchmark_quicksort, @function
benchmark_quicksort:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	a1,16(sp)
	addi	s0,sp,32
	sd	t2,-24(s0)
	li	a2,99
	li	a1,0
	ld	a0,-24(s0)
	call	quicksort
	nop
	ld	ra,24(sp)
	ld	s0,16(sp)
	addi	sp,sp,32
	jr	ra
	.size	benchmark_quicksort, .-benchmark_quicksort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	mv	s4,t1
	sd	t5,56(sp)
	sd	s4,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	addw	a6,a5,s8
	sll	t5,s10,s1
	sra	a6,t4,s9
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L17
	sw	zero,-36(s0)
	j	.L18
.L19:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	sp,a4,a5
	lw	a4,-36(s0)
	sw	a4,0(sp)
	sllw	s8,a6,s6
	addi	s6,a2,1933
	mul	t4,s5,t6
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L18:
	lw	a5,-36(s0)
	sext.w	a4,a5
	mv	ra,a4
	li	a5,99
	ble	ra,a5,.L19
	j	.L20
.L17:
	sw	zero,-36(s0)
	j	.L21
.L22:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	sraiw	t6,t0,4
	slti	s6,s6,1019
	subw	t4,s7,a0
	mv	a5,a0
	sw	a5,0(s1)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L21:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L22
.L20:
	nop
	sra	s4,s10,s8
	mv	ra,a2
	addiw	s10,a6,-355
	mulh	t1,ra,t5
	mv	a0,a5
	ld	ra,56(sp)
	mulw	s5,s11,a7
	mv	a1,sp
	sllw	s6,s5,s7
	add	t6,a6,a6
	ld	s0,48(a1)
	ld	s1,40(a1)
	addi	sp,a1,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	a0,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	li	a1,0
	mv	a0,a5
	call	fill_array
	lw	a5,-20(s0)
	mv	a0,a5
	call	benchmark_quicksort
	srli	a6,a0,12
	mv	s7,a7
	mulhsu	t3,t1,s7
	lw	a5,-20(s0)
	mv	a0,a5
	call	free
	li	a5,0
	mv	a0,a5
	ld	ra,24(sp)
	ld	s0,16(sp)
	addi	sp,sp,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
