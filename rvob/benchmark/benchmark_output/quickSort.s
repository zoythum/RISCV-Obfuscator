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
	lw	ra,0(a5)
	ld	a5,-40(s0)
	sw	ra,0(a5)
	ld	a5,-48(s0)
	lw	a4,-20(s0)
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
	sw	a5,-44(s0)
	mv	a5,a4
	sw	a5,-48(s0)
	lw	a5,-44(s0)
	sw	a5,-20(s0)
	lw	a5,-48(s0)
	sw	a5,-24(s0)
	lw	a5,-44(s0)
	slli	ra,a5,2
	ld	a4,-40(s0)
	add	a5,a4,ra
	lw	a5,0(ra)
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
	mv	t2,a4
	lw	a5,-28(s0)
	sext.w	a5,a5
	bgt	a5,t2,.L8
	j	.L9
.L10:
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L9:
	lw	a5,-24(s0)
	slli	a5,a5,2
	ld	a4,-40(s0)
	add	a5,a4,a5
	lw	a4,0(a5)
	lw	a5,-28(s0)
	sext.w	a5,a5
	blt	a5,a4,.L10
	lw	a4,-20(s0)
	lw	ra,-24(s0)
	srlw	s4,ra,t0
	mulhsu	t2,t3,a6
	slt	t6,a6,t2
	sext.w	a4,a4
	sext.w	a5,ra
	bgt	a4,ra,.L6
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
	addiw	a5,a5,1
	sw	a5,-20(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,-1
	sw	a5,-24(s0)
.L6:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	mv	ra,a5
	sext.w	t1,a4
	sext.w	a5,ra
	ble	t1,a5,.L7
	lw	a4,-44(s0)
	lw	a5,-24(s0)
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
	call	quicksort
.L14:
	nop
	ld	ra,40(sp)
	ld	s0,32(sp)
	mv	t0,ra
	addi	sp,sp,48
	jr	t0
	.size	quicksort, .-quicksort
	.align	1
	.globl	benchmark_quicksort
	.type	benchmark_quicksort, @function
benchmark_quicksort:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sd	s0,16(sp)
	mulhu	s10,t0,t5
	sllw	s9,a4,a1
	mulh	t2,s6,t3
	srai	t6,s4,2
	srliw	s4,t6,9
	xor	s3,s6,a3
	addi	s0,sp,32
	sd	t1,-24(s0)
	li	a2,99
	li	a1,0
	ld	a0,-24(s0)
	call	quicksort
	nop
	ld	ra,24(sp)
	mv	t0,sp
	ld	s0,16(t0)
	addi	sp,t0,32
	jr	ra
	.size	benchmark_quicksort, .-benchmark_quicksort
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	mv	s3,s0
	sd	ra,56(sp)
	mv	s2,s9
	sd	s3,48(sp)
	sd	s1,40(sp)
	addi	s0,sp,64
	sltiu	a2,t3,1396
	or	t4,s2,t4
	xori	a2,s2,-691
	sd	a0,-56(s0)
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
	mv	ra,a5
	ld	a4,-56(s0)
	add	a5,a4,ra
	lw	a4,-36(s0)
	sw	a4,0(a5)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	sw	a5,-36(s0)
.L18:
	lw	a5,-36(s0)
	sext.w	a4,a5
	li	a5,99
	mv	ra,a4
	add	s10,t3,a3
	slt	s7,a6,t2
	addiw	s10,t5,-787
	ble	ra,a5,.L19
	j	.L20
.L17:
	sw	zero,-36(s0)
	j	.L21
	sllw	a3,t3,s2
	srl	s9,a3,a3
	xor	s5,t1,a7
	mulw	t5,ra,s5
	sltu	s6,t3,s10
	add	a6,t6,t0
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
	srliw	s7,s5,15
	and	ra,s11,s7
	sltu	ra,a1,t3
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
main:
	addi	sp,sp,-32
	sd	ra,24(sp)
	sub	t1,s6,t2
	sltu	t6,ra,a0
	srlw	s0,s10,a4
	sd	s0,16(sp)
	addi	s0,sp,32
	li	a0,400
	call	malloc
	mv	a5,a0
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	li	a1,0
	addw	s11,s9,a4
	sll	s0,a7,t4
	mv	ra,a5
	slli	a2,a4,12
	mv	a0,ra
	call	fill_array
	lw	a5,-20(s0)
	mv	a0,a5
	call	benchmark_quicksort
	lw	a5,-20(s0)
	mv	t1,t0
	mv	a0,a5
	sltu	t4,a2,t6
	addi	a7,t5,-86
	slti	s5,s9,-1729
	mv	s8,t1
	srliw	s3,a7,14
	slti	s7,a2,-69
	call	free
	li	a5,0
	mv	a0,a5
	ld	ra,24(sp)
	ld	s0,16(sp)
	addi	sp,sp,32
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
