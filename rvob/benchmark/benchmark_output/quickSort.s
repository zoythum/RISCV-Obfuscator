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
	sd	a1,-48(s0)
	ld	a5,-40(s0)
	lw	a5,0(a5)
	sw	a5,-20(s0)
	ld	a5,-48(s0)
	lw	a4,0(a5)
	ld	a5,-40(s0)
	sw	a4,0(a5)
	mv	ra,s0
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
	sd	ra,40(sp)
	sd	s0,32(sp)
	addi	s0,sp,48
	sd	a0,-40(s0)
	mv	a5,a1
	mv	a4,a2
	addi	s8,t4,1031
	srai	t1,s9,20
	mv	ra,a4
	mv	s11,t6
	sw	a5,-44(s0)
	mv	a5,ra
	sw	a5,-48(s0)
	lw	a5,-44(s0)
	sw	a5,-20(s0)
	lw	a5,-48(s0)
	sw	a5,-24(s0)
	lw	a5,-44(s0)
	slli	a5,a5,2
	xor	a6,s6,s4
	mulw	s6,a3,a7
	addi	t2,a6,1647
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
	srlw	s5,t6,s7
	mul	t2,s4,t0
	addiw	s10,a7,601
	slli	ra,a5,2
	ld	a4,-40(s0)
	add	a5,a4,ra
	lw	s1,0(ra)
	lw	a5,-28(s0)
	sext.w	a5,a5
	bgt	a5,s1,.L8
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
	lw	a4,0(ra)
	lw	a5,-28(s0)
	sext.w	a5,a5
	blt	a5,a4,.L10
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	mv	sp,a5
	sext.w	a4,a4
	sext.w	a5,sp
	bgt	a4,a5,.L6
	lw	a5,-20(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a3,a4,a5
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	mv	a1,a5
	mv	a0,a3
	call	swap
	lw	a5,-20(s0)
	slti	s8,s6,1678
	sltiu	s11,s6,-474
	sll	s2,s6,s3
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
	sext.w	a4,a4
	sext.w	a5,a5
	bge	a4,a5,.L12
	sllw	t2,t1,a3
	slt	s3,s11,t6
	addiw	s2,s5,826
	lw	a4,-24(s0)
	lw	a5,-44(s0)
	mv	a2,a4
	mv	a1,a5
	ld	a0,-40(s0)
	call	quicksort
.L12:
	lw	ra,-20(s0)
	lw	sp,-48(s0)
	sext.w	a4,ra
	sext.w	a5,sp
	bge	a4,sp,.L14
	lw	a4,-48(s0)
	srl	s2,s9,t4
	sltu	a3,t0,a3
	mulhsu	a1,s10,s4
	lw	a5,-20(s0)
	mv	a2,a4
	mv	a1,a5
	ld	a0,-40(s0)
	call	quicksort
.L14:
	nop
	ld	ra,40(sp)
	mv	t0,ra
	ld	s0,32(sp)
	addi	sp,sp,48
	jr	t0
	.size	quicksort, .-quicksort
	.align	1
	.globl	benchmark_quicksort
	.type	benchmark_quicksort, @function
benchmark_quicksort:
	addi	sp,sp,-32
	mv	t1,s0
	sd	ra,24(sp)
	sd	t1,16(sp)
	addi	s0,sp,32
	sd	t2,-24(s0)
	li	a2,99
	li	a1,0
	ld	a0,-24(s0)
	call	quicksort
	srai	t1,s11,16
	sllw	a0,a2,s9
	mv	t1,t2
	nop
	ld	ra,24(sp)
	mv	a5,ra
	mv	s1,sp
	ld	s0,16(s1)
	addi	sp,s1,32
	jr	a5
	.size	benchmark_quicksort, .-benchmark_quicksort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	sd	ra,56(sp)
	sd	s0,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sd	a0,-56(s0)
	mv	a5,a1
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L17
	sltiu	a6,t1,877
	slli	ra,t0,20
	sll	s7,a3,t1
	sw	zero,-36(s0)
	j	.L18
.L19:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	a5,a4,a5
	lw	a4,-36(s0)
	sw	a4,0(a5)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
	srli	t6,s11,27
	or	s11,a4,t5
	add	t1,s8,s1
.L18:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	ble	a4,a5,.L19
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
	mv	a0,a5
	ld	ra,56(sp)
	ld	s0,48(sp)
	ld	s1,40(sp)
	addi	sp,sp,64
	jr	ra
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
	slt	s8,t5,ra
	mv	t2,a0
	slti	s6,s3,-1159
	sll	ra,t2,s5
main:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	mv	s2,a0
	add	s9,t0,a7
	xori	a1,s9,1994
	and	a2,s10,a6
	xor	t2,ra,t0
	or	s1,s2,t3
	srlw	t3,t3,s9
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
	mv	a0,a5
	ld	ra,24(t2)
	ld	s0,16(t2)
	addi	sp,t2,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
